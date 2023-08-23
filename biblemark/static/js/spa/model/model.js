import Mark from "./mark.js";
import MarkedVerse from "./markedVerse.js";

export default class Model {

    constructor() {
        /**
         * @type {string}
         */
        this.title = '';

        /**
         * @type {string}
         */
        this.content = '';

        /**
         * @type {[VersionResponseItem]}
         */
        this.versions = [];

        /**
         * @type {string}
         */
        this.versionId = '';

        /**
         * @type {[BookResponseItem]}
         */
        this.books = [];

        /**
         * @type {string}
         */
        this.bookId = '';

        /**
         * @type {[ChapterResponseItem]}
         */
        this.chapters = [];

        /**
         * @type {string}
         */
        this.chapterId = '';

        /**
         * @type {{}}
         */
        this.prev = {};

        /**
         * @type {{}}
         */
        this.next = {};

        /**
         * @type {Map<string, Mark>}
         */
        this.marksById = new Map();

        /**
         * @typedef MarksByType
         * @type {object}
         * @property {Map<string, [Mark]>} highlights - Highlight marks associated by color code
         * @property {[Mark]} notes - Note marks
         */

        /**
         * @type {Map<VersionedVerseId, MarksByType>}
         */
        this.marksByTypeByVersionedVerseId = new Map();

        /**
         * @type {Set<VersionedVerseId>}
         * @private
         */
        this._selection = new Set();
    }

    /**
     * @param {VersionedVerseId} versionedVerseId
     */
    addSelectedVerse = versionedVerseId => {
        this._selection.add(versionedVerseId);
    }

    /**
     * @param {VersionedVerseId} versionedVerseId
     */
    removeSelectedVerse = versionedVerseId => {
        this._selection.delete(versionedVerseId);
    }

    toggleVerseSelect = (versionedVerseId) => {
        this._selection.has(versionedVerseId)
            ? this.removeSelectedVerse(versionedVerseId)
            : this.addSelectedVerse(versionedVerseId);
    }

    clearSelection = () => {
        this._selection.clear();
    }

    /**
     * @returns {Set<VersionedVerseId>}
     */
    getSelection = () => this._selection;

    /**
     * @returns {Map<VersionedVerseId, MarksByType>}
     */
    getMarksByTypeByVersionedVerseId = () => this.marksByTypeByVersionedVerseId;

    /**
     * @returns {MarksByType}
     */
    getSelectedMarks() {
        return this.getMarksInVerses(this.getSelection());
    }

    /**
     * @param {[Mark]} marks
     */
    setMarks = marks => {
        if (!Array.isArray(marks)) {
            console.error("Invalid marks data");
            return;
        }

        this.marksById.clear();
        this.marksByTypeByVersionedVerseId.clear();

        marks.forEach(mark => {
            this.addMark(mark);
        });
    }

    /**
     * @param {Mark} mark
     */
    addMark = mark => {
        if (!mark instanceof Mark) {
            console.error("Invalid mark data");
            return;
        }

        this.marksById.set(mark.id, mark);

        mark.markedVerses.forEach(markedVerse => {
            if (!markedVerse instanceof MarkedVerse) {
                console.warn("Invalid marked verse data");
                return;
            }

            const versionedVerseId = markedVerse.verse.toVersionedId();

            let {
                highlights = new Map(), notes = []
            } = this.marksByTypeByVersionedVerseId.get(versionedVerseId) || {};

            if (mark.color) highlights.set(mark.color, [...(highlights.get(mark.color) || []), mark]);
            if (mark.note) notes.push(mark);

            this.marksByTypeByVersionedVerseId.set(versionedVerseId, { highlights, notes });
        });
    }

    /**
     * @param {Set<VersionedVerseId>} versionedVerseIds
     * @returns {MarksByType}
     */
    getMarksInVerses = (versionedVerseIds) => {
        let highlights = new Map();
        let notes = new Set();

        [...versionedVerseIds.values()].flatMap(versionedVerseId =>
            this.marksByTypeByVersionedVerseId.has(versionedVerseId)
                ? this.marksByTypeByVersionedVerseId.get(versionedVerseId)
                : []
        ).forEach(verseMarksByType => {
            verseMarksByType.highlights.forEach((marks, color) => {
                if (!highlights.has(color)) {
                    highlights.set(color, new Set());
                }
                marks.forEach(mark => highlights.get(color).add(mark));
            });

            verseMarksByType.notes.forEach(note => notes.add(note));
        });

        return { highlights, notes }
    }

    /**
     * Removes highlighted verses, and the highlight mark in case of empty marked verses.
     * @param {string} highlightedId
     * @param {string} highlightedVerseId
     */
    deleteHighlightedVerseById = (highlightedId, highlightedVerseId) => {
        const highlightMark = this.marksById.get(highlightedId);

        if (!highlightMark) {
            console.error(`No highlight mark found with ID ${highlightedId}`);
            return;
        }

        const markedVerse = [...highlightMark.markedVerses.values()].find(markedVerse => markedVerse.id === highlightedVerseId);

        if (!markedVerse) {
            console.error(`No marked verse found at mark ID ${highlightedId}`);
            return;
        }

        const versionedVerseId = markedVerse.verse.toVersionedId();
        const verseMarks = this.marksByTypeByVersionedVerseId.get(versionedVerseId);

        if (!verseMarks) {
            console.error(`No marks found for verse ID ${versionedVerseId}`);
            return;
        }

        // Remove the mark or marked verse
        if (highlightMark.markedVerses.size === 1) {
            // Remove entire mark
            highlightMark.markedVerses.forEach(markedVerse => {
                const versionedVerseId = markedVerse.verse.toVersionedId();
                const verseMarks = this.marksByTypeByVersionedVerseId.get(versionedVerseId);
                verseMarks.highlights.delete(highlightMark.color);
            });
            this.marksById.delete(highlightedId);
        } else {
            // Remove only the marked verse
            highlightMark.markedVerses.delete(versionedVerseId);
            verseMarks.highlights.delete(highlightMark.color);
        }
    }

    /**
     * @param {string} noteId
     */
    deleteNoteById = noteId => {
        const noteMark = this.marksById.get(noteId);

        if (noteMark) {
            noteMark.markedVerses.forEach(markedVerse => {
                const versionedVerseId = markedVerse.verse.toVersionedId();
                const verseMarksByType = this.marksByTypeByVersionedVerseId.get(versionedVerseId);

                if (verseMarksByType) {
                    verseMarksByType.notes = verseMarksByType.notes.filter(mark => mark.id !== noteId);
                } else {
                    console.error(`No marks found at verse ID ${versionedVerseId}`);
                }
            });

            this.marksById.delete(noteId);
        } else {
            console.error(`No note mark found with ID ${noteId}`);
        }
    }
}