import Verse from "../model/verse.js";

const MARKABLE_CLASS = 'markable';

const VERSE_HOVER_CLASS = 'hover';
const VERSE_SELECTED_CLASS = 'selected';

const VERSE_HIGHLIGHT_CLASS = 'highlighted';
const VERSE_NOTE_CLASS = 'noted';

/**
 * Time in milliseconds to wait before auto saving note after user input.
 * @type {number}
 */
const NOTE_AUTOSAVE_DEBOUNCE_TIME = 600;

/**
 * Size in pixels determining breakpoint between small and large screens.
 *
 * Needs to match CSS media query.
 *
 * @type {number}
 */
const LARGE_SCREEN_BREAKPOINT = 992;

/**
 * Gap in pixels between note content elements.
 * @type {number}
 */
const NOTE_GAP = 30;

/**
 * Height in pixels to limit note content element.
 * @type {number}
 */
const NOTE_BODY_MAX_HEIGHT = 150;

/**
 * View for scripture content and marking rendering, including notes.
 */
export default class BibleView {

    constructor() {

        /**
         * @type {Map<VersionedVerseId, [HTMLElement]>}
         */
        this.verses = new Map();

        /**
         * @type {Map<VersionedVerseId, [HTMLElement]>}
         */
        this.selection = new Map();

        /**
         * Represents the relationship between verse number and note content element.
         * @typedef AnchoredNote
         * @type {object}
         * @property {number} verseNumber - Verse number
         * @property {HTMLElement} anchorElement - Verse number element
         * @property {HTMLElement} noteElement - Note content element
         */

        /**
         * @type {Map<string, AnchoredNote>} {@link AnchoredNote} by note ID
         */
        this.anchoredNotesByNoteId = new Map();

        this.container = document.getElementById('scripture-container');
        this.title = document.getElementById('scripture-reference');
        this.content = document.getElementById('scripture-content');
        this.spinner = document.getElementById('scripture-spinner');

        this.leftNotePanel = document.getElementById('note-panel-left');
        this.rightNotePanel = document.getElementById('note-panel-right');
        this.mergedNotePanel = document.getElementById('note-panel-merged');

        this.noteTemplate = document.getElementById('note-template');

        window.addEventListener('resize', _ => this._renderNoteContentElements());
    }

    // bindings

    /**
     * @param {toggleVerseHoverHandlerCallback} handler
     */
    bindToggleVerseHover = handler => this.toggleVerseHoverHandler = handler;

    /**
     * @param {toggleVerseSelectionHandlerCallback} handler
     */
    bindToggleVerseSelection = handler => this.toggleVerseSelectionHandler = handler;

    /**
     * @param {editNoteHandlerCallback} handler
     */
    bindEditNote = handler => this.editNoteHandler = handler;

    /**
     * @param {deleteNoteHandlerCallback} handler
     */
    bindDeleteNote = handler => this.deleteNoteHandler = handler;

    // clearing

    /**
     * Removes all rendered verse elements, and related internal mapping.
     */
    clearContent = () => {
        this.content.innerHTML = '';
        this.verses.clear();
    }

    /**
     * Removes all applied selected styles, and related internal mapping.
     */
    clearSelection = () => {
        this.selection.forEach(verseElements => {
            verseElements.forEach(verseElement => {
               verseElement.classList.remove(VERSE_SELECTED_CLASS);
            });
        });

        this.selection.clear();
    }

    /**
     * Removes all applied mark styles from verses, note content, and related internal mapping.
     */
    clearMarks = () => {
        this.clearMarkStyles();
        this.clearNoteContent();

        this.anchoredNotesByNoteId.clear();
    }

    /**
     * Removes all applied mark styles from verses.
     */
    clearMarkStyles = () => {
        this.verses.forEach(verseElements => {
            verseElements.forEach(verseElement => {
                verseElement.classList.remove(VERSE_HIGHLIGHT_CLASS, VERSE_NOTE_CLASS);
                verseElement.style.backgroundColor = 'unset';
            })
        });
    }

    /**
     * Removes all rendered note content.
     */
    clearNoteContent = () => {
        this.leftNotePanel.querySelector('.note-panel-body').innerHTML = '';
        this.mergedNotePanel.querySelector('.note-panel-body').innerHTML = '';
        this.rightNotePanel.querySelector('.note-panel-body').innerHTML = '';
    }

    // interaction

    /**
     * @param {boolean} isMarkable
     */
    setMarkable = isMarkable => {
        isMarkable
        ? this.content.classList.add(MARKABLE_CLASS)
        : this.content.classList.remove(MARKABLE_CLASS);
    };

    /**
     * @param {VersionedVerseId} versionedVerseId
     */
    toggleVerseHover = versionedVerseId => {
        this.verses.get(versionedVerseId).forEach(verseElement => {
            verseElement.classList.toggle(VERSE_HOVER_CLASS);
        });
    }

    /**
     * @param {VersionedVerseId} versionedVerseId
     */
    toggleVerseSelection = versionedVerseId => {
        this.selection.has(versionedVerseId)
            ? this.selection.delete(versionedVerseId)
            : this.selection.set(versionedVerseId, this.verses.get(versionedVerseId));

        this.verses.get(versionedVerseId).forEach(verseElement => {
            verseElement.classList.toggle(VERSE_SELECTED_CLASS);
        });
    }

    // user feedback

    startLoading = () => {
        this.spinner.classList.remove('visually-hidden');
        this.container.classList.add('invisible');
    }

    stopLoading = () => {
        this.spinner.classList.add('visually-hidden');
        this.container.classList.remove('invisible');
    }

    /**
     * @param {string} noteId
     * @param {string} status
     */
    updateNoteStatus = (noteId, status) => {
        this.anchoredNotesByNoteId.get(noteId).noteElement.querySelector('.note-status').innerText = status;
    }

    /**
     * @param {string} noteId
     */
    enableNoteDeletion = (noteId) => {
        this.anchoredNotesByNoteId.get(noteId).noteElement.querySelector('.btn-close').disabled = false;
    }

    // rendering

    /**
     * @param {string} versionId
     * @param {string} title
     * @param {string} content - HTML code for the content
     */
    renderContent(versionId, title, content) {
        this.clearContent();

        this.title.innerHTML = title;
        this.content.innerHTML = content;

        const verseElements = this.content.querySelectorAll(`[data-verse-id]`);

        verseElements.forEach(verseElement => {
            const versionedVerseId = Verse.generateVersionedId(versionId, verseElement.dataset.verseId);

            if (this.verses.has(versionedVerseId)) {
                this.verses.get(versionedVerseId).push(verseElement);
            } else {
                this.verses.set(versionedVerseId, [verseElement]);
            }

            // avoiding hover event because of multiple verse elements
            verseElement.addEventListener('mouseenter', event => { this._onHoverVerse(event); });
            verseElement.addEventListener('mouseleave', event => { this._onHoverVerse(event); });

            verseElement.addEventListener('click', event => { this._onClickVerse(event); });
        });
    }

    /**
     * Renders mark styles and note content elements, completely re-rendering existent items.
     * @param {Map<VersionedVerseId, MarksByType>} marksByTypeByVersionedVerseId
     */
    renderMarks(marksByTypeByVersionedVerseId) {
        this.clearMarks();
        this._renderMarkStyles(marksByTypeByVersionedVerseId);
        this._createNoteContentElements(marksByTypeByVersionedVerseId);
        this._renderNoteContentElements();
    }

    /**
     * Renders highlight and note marks by applying defined styles in verse elements.
     *
     * For highlights, the style is applied to every element that belongs to the verses.
     *
     * For notes, it is only applied to the verse number element of the first verse of the related verse group.
     *
     * @param {Map<VersionedVerseId, MarksByType>} marksByTypeByVersionedVerseId
     * @private
     */
    _renderMarkStyles = (marksByTypeByVersionedVerseId) => {
        marksByTypeByVersionedVerseId.forEach((marksByType, versionedVerseId) => {
            const verseElements = this.verses.get(versionedVerseId);

            const highlight = [...marksByType.highlights.values()].flat().find(mark =>
                mark.markedVerses.has(versionedVerseId));

            verseElements.forEach(verseElement => {
                if (highlight) {
                    verseElement.classList.add(VERSE_HIGHLIGHT_CLASS);
                    verseElement.style.backgroundColor = highlight.color;
                }

                const isVerseNumberElement = verseElements.indexOf(verseElement) === 0;

                if (isVerseNumberElement) {
                    if (marksByType.notes.length > 0) {
                        verseElement.classList.add(VERSE_NOTE_CLASS);
                    }
                }
            });
        });
    }

    /**
     * Creates note content elements and stores relationship with the verse number element.
     *
     * @param {Map<VersionedVerseId, MarksByType>} marksByTypeByVersionedVerseId
     * @private
     */
    _createNoteContentElements = (marksByTypeByVersionedVerseId) => {
        const processedNotes = new Set();

        marksByTypeByVersionedVerseId.forEach((marksByType, versionedVerseId) => {
            const [verseNumberElement] = this.verses.get(versionedVerseId);

            if (marksByType.notes.length > 0) {
                marksByType.notes.forEach(noteMark => {
                    if (!processedNotes.has(noteMark.id)) {
                        processedNotes.add(noteMark.id);

                        this.anchoredNotesByNoteId.set(noteMark.id, {
                            verseNumber: Verse.parseVersionedVerseId(versionedVerseId).verseNumber,
                            anchorElement: verseNumberElement,
                            noteElement: this._createNoteContentElement(noteMark),
                        });
                    }
                });
            }
        });
    }

    /**
     * Renders note content elements.
     *
     * Note content elements are rendered at the footer in small screens according to the `LARGE_SCREEN_BREAKPOINT`,
     * or in the anchor's nearest side panel in large screens, vertically aligned with the verse number element,
     * detecting and solving collisions.
     *
     * @private
     */
    _renderNoteContentElements = () => {
        this.clearNoteContent();

        const notePanels = {
            left: this.leftNotePanel.querySelector('.note-panel-body'),
            right: this.rightNotePanel.querySelector('.note-panel-body'),
            merged: this.mergedNotePanel.querySelector('.note-panel-body')
        };

        /**
         * @param {HTMLElement} panel
         * @param {HTMLElement} anchor
         * @param {number} gap
         * @returns {number}
         */
        const calculateYOffset = (panel, anchor, gap) => {
            const anchorBottom = anchor.offsetTop + anchor.clientHeight;
            const previousNote = panel.lastChild;

            if (previousNote) {
                const previousNoteBottom = previousNote.offsetTop + previousNote.clientHeight;
                return Math.max(anchorBottom + gap, previousNoteBottom + gap);
            }

            return anchorBottom + gap;
        };

        [...this.anchoredNotesByNoteId.values()].sort(
            (a, b) => a.verseNumber - b.verseNumber
        ).forEach(anchoredNote => {
            if (window.innerWidth < LARGE_SCREEN_BREAKPOINT) {
                anchoredNote.noteElement.style.top = 'unset';
                notePanels.left.style.height = 'unset';
                notePanels.right.style.height = 'unset';
                notePanels.merged.appendChild(anchoredNote.noteElement);
            } else {
                const middle = this.content.offsetLeft + this.content.clientWidth / 2;
                const targetPanel = anchoredNote.anchorElement.offsetLeft > middle ? notePanels.right : notePanels.left;
                const yOffset = calculateYOffset(targetPanel, anchoredNote.anchorElement, NOTE_GAP);

                anchoredNote.noteElement.style.top = `${yOffset}px`;
                targetPanel.appendChild(anchoredNote.noteElement);

                const noteBody = anchoredNote.noteElement.querySelector('.note-body');
                const initialHeight = Math.min(noteBody.clientHeight, NOTE_BODY_MAX_HEIGHT);
                noteBody.style.maxHeight = `${initialHeight}px`;

                targetPanel.style.height = `${yOffset + anchoredNote.noteElement.clientHeight + NOTE_GAP}px`;
            }
        });
    }

    /**
     * Creates an editable and deletable element to display note content.
     *
     * The element contains:
     * - header containing title and delete button (click triggers event)
     * - body, editable (input triggers event)
     *
     * @param {Mark} mark
     * @returns {HTMLElement}
     * @private
     */
    _createNoteContentElement = mark => {
        const noteContent = this.noteTemplate.content.cloneNode(true).querySelector('.note');

        noteContent.dataset.id = mark.id;
        noteContent.querySelector('.note-header .note-reference').innerText = mark.reference;

        const deleteBtn = noteContent.querySelector('.note-header .btn-close');
        deleteBtn.addEventListener('click', (event) => this._onDeleteNote(event, mark.id));

        const noteBody = noteContent.querySelector('.note-body');
        noteBody.contentEditable = true;
        noteBody.innerText = mark.note;
        noteBody.addEventListener('input', (event) => this._onEditNote(event, mark.id));

        return noteContent;
    }

    // event listeners

    /**
     * @param {Event} event
     * @private
     */
    _onHoverVerse = event => {
        const verseId = event.target.closest('[data-verse-id]').dataset.verseId;
        this.toggleVerseHoverHandler(verseId);
    }

    /**
     * @param {Event} event
     * @private
     */
    _onClickVerse = event => {
        const verseId = event.target.closest('[data-verse-id]').dataset.verseId;
        this.toggleVerseSelectionHandler(verseId);
    }

    /**
     * @param {Event} event
     * @param {string} noteId
     * @private
     */
    _onEditNote = (event, noteId) => {
        clearTimeout(this.autosaveTimeout);
        this.autosaveTimeout = setTimeout(() => {
            this.editNoteHandler(noteId, event.target.textContent);
        }, NOTE_AUTOSAVE_DEBOUNCE_TIME);
    }

    /**
     * @param {Event} event
     * @param {string} noteId
     * @private
     */
    _onDeleteNote = (event, noteId) => {
        event.target.disabled = true;
        this.deleteNoteHandler(noteId);
    }
}