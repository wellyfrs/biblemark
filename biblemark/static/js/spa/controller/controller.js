import Mark from "../model/mark.js";
import MarkedVerse from "../model/markedVerse.js";
import Verse from "../model/verse.js";

export default class Controller {

    /**
     * @param {Model} model
     * @param {View} view
     * @param {Client} client
     */
    constructor(model, view, client) {
        this.model = model;
        this.view = view;
        this.client = client;

        this.view.nav.bindChangeVersion(this.handleChangeVersion);
        this.view.nav.bindChangeBook(this.handleChangeBook);
        this.view.nav.bindChangeChapter(this.handleChangeChapter);
        this.view.nav.bindNavNext(this.handleNavNext);
        this.view.nav.bindNavPrev(this.handleNavPrev);

        this.view.bible.bindToggleVerseHover(this.handleToggleVerseHover);
        this.view.bible.bindToggleVerseSelection(this.handleToggleVerseSelection);
        this.view.bible.bindEditNote(this.handleNoteEdit);
        this.view.bible.bindDeleteNote(this.handleDeleteNote);

        this.view.control.bindHighlightAction(this.handleHighlightAction);
        this.view.control.bindAddNoteAction(this.handleAddNote);

        this.client.fetchMe().then(() => {
            this.hasAuthenticatedUser = true;
        }).catch(() => {
            this.hasAuthenticatedUser = false;
        }).finally(() => {
            this.view.bible.setMarkable(this.hasAuthenticatedUser);
        });
    }

    /**
     * @param {string} versionId
     * @param {string} bookId
     * @param {string} chapterId
     */
    init = (versionId, bookId, chapterId) => {
        this.client.fetchVersions()
            .then(response => {
                this.model.versions = response.versions;
                this.view.nav.renderVersionSelectElement(this.model.versions, versionId);
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                console.error(error);
            });

        this.client.fetchBooks(versionId)
            .then(response => {
                this.model.books = response.books;
                this.view.nav.renderBookSelectElement(this.model.books, bookId);
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                console.error(error);
            });

        this.client.fetchChapters(versionId, bookId)
            .then(response => {
                this.model.chapters = response.chapters;
                this.view.nav.renderChapterSelectElement(this.model.chapters, chapterId);
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                console.error(error);
            });

        this.goTo(versionId, bookId, chapterId);
    }

    /**
     * @param versionId
     * @param bookId
     * @param chapterId
     * @returns Promise<any>
     */
    goTo = (versionId, bookId, chapterId) => {
        this.view.nav.disableAllSelectElements();
        this.view.bible.startLoading();

        return this.client.fetchChapter(versionId, bookId, chapterId)
            .then(async response => {
                this.model.versionId = response.chapter.versionId;
                this.model.bookId = response.chapter.bookId;
                this.model.chapterId = response.chapter.chapterId;

                this.model.prev = response._links.prev;
                this.model.next = response._links.next;

                this.model.title = response.chapter.reference;
                this.model.content = response.chapter.content;

                history.pushState(null, '', response._links.self.href);
                this.view.bible.renderContent(this.model.versionId, this.model.title, this.model.content);

                if (this.hasAuthenticatedUser) {
                    await this.client.fetchChapterMarks(versionId, bookId, chapterId).then(response => {
                        this.model.setMarks(response.marks.map(Mark.fromMarkResponse));
                    });
                } else {
                    this.model.setMarks([]);
                }

                this.view.bible.renderMarks(this.model.getMarksByTypeByVersionedVerseId());
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                console.error(error);
            }).finally(() => {
                this.view.nav.enableAllSelectElements();
                this.view.bible.stopLoading();
            });
    }

    /**
     * @callback changeVersionHandlerCallback
     * @param {string} versionId
     */
    handleChangeVersion = versionId => {
        this.goTo(versionId, this.model.bookId, this.model.chapterId);
    }

    /**
     * @callback changeBookHandlerCallback
     * @param {string} bookId
     */
    handleChangeBook = bookId => {
        this.model.bookId = bookId;
        this.view.nav.disableAllSelectElements();
        this.client.fetchChapters(this.model.versionId, this.model.bookId)
            .then(response => {
                this.model.chapters = response.chapters;
                this.view.nav.renderChapterSelectElement(this.model.chapters, this.model.chapters[0].id);
                this.view.nav.enableAllSelectElements();
                this.view.nav.chapter.focus();
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                this.view.nav.enableAllSelectElements();
                console.error(error);
            });
    }

    /**
     * @callback changeChapterHandlerCallback
     * @param {string} chapterId
     */
    handleChangeChapter = chapterId => {
        this.goTo(this.model.versionId, this.model.bookId, chapterId);
    }

    /**
     * @callback navPrevHandlerCallback
     */
    handleNavPrev = () => {
        this.view.nav.disableAllSelectElements();
        this.goTo(
            this.model.prev.versionId,
            this.model.prev.bookId,
            this.model.prev.chapterId,
        ).then(_ => {
            this.view.nav.renderBookSelectElement(this.model.books, this.model.bookId);
            this.view.nav.renderChapterSelectElement(this.model.chapters, this.model.chapterId);
            this.view.nav.enableAllSelectElements();
        });
    }

    /**
     * @callback navNextHandlerCallback
     */
    handleNavNext = () => {
        this.view.nav.disableAllSelectElements();
        this.goTo(
            this.model.next.versionId,
            this.model.next.bookId,
            this.model.next.chapterId,
        ).then(_ => {
            this.view.nav.renderBookSelectElement(this.model.books, this.model.bookId);
            this.view.nav.renderChapterSelectElement(this.model.chapters, this.model.chapterId);
            this.view.nav.enableAllSelectElements();
        });
    }

    /**
     * @callback toggleVerseHoverHandlerCallback
     * @param {VerseId} verseId
     */
    handleToggleVerseHover = verseId => {
        if (!this.hasAuthenticatedUser) return;
        const versionedVerseId = Verse.generateVersionedId(this.model.versionId, verseId);
        this.view.bible.toggleVerseHover(versionedVerseId);
    }

    /**
     * @callback toggleVerseSelectionHandlerCallback
     * @param {VerseId} verseId
     */
    handleToggleVerseSelection = verseId => {
        if (!this.hasAuthenticatedUser) return;
        const versionedVerseId = Verse.generateVersionedId(this.model.versionId, verseId);
        this.view.bible.toggleVerseSelection(versionedVerseId);
        this.model.toggleVerseSelect(versionedVerseId);
        this._updateMarkingControlDisplay();
    }

    /**
     * @callback highlightActionHandlerCallback
     * @param {string} selectedColorCode
     */
    handleHighlightAction = selectedColorCode => {
        const selectedMarks = this.model.getSelectedMarks();

        if (selectedMarks.highlights.size > 0) {
            if (selectedMarks.highlights.has(selectedColorCode)) {
                this._removeHighlights(selectedColorCode, selectedMarks);
            } else {
                this._replaceHighlights(selectedColorCode, selectedMarks);
            }
        } else {
            this._saveHighlight(selectedColorCode);
        }
    }

    /**
     * @callback addNoteHandlerCallback
     * @param {string} note
     */
    handleAddNote = note => {
        const markedVerses = [...this.model.getSelection().values()].map(v => MarkedVerse.fromVersionedVerseId(v));
        const mark = Mark.factory(null, note, markedVerses);
        this._saveMark(mark)
            .then(_ => {
                this.view.bible.renderMarks(this.model.getMarksByTypeByVersionedVerseId());
                this.model.clearSelection();
                this.view.bible.clearSelection();
                this._updateMarkingControlDisplay();
            });
    }

    /**
     * @callback editNoteHandlerCallback
     * @param {string} noteId
     * @param {string} text
     */
    handleNoteEdit = (noteId, text) => {
        this.view.bible.updateNoteStatus(noteId, 'Saving...');
        this.client.patchMark(noteId, { note: text })
            .then(response => {
                this.view.bible.updateNoteStatus(noteId, '');
            }).catch(error => {
                this.view.bible.updateNoteStatus(noteId, 'Error');
            });
    }

    /**
     * @callback deleteNoteHandlerCallback
     * @param {string} noteId
     */
    handleDeleteNote = noteId => {
        this.client.deleteMark(noteId)
            .then(response => {
                this.model.deleteNoteById(response.id);
                this.view.bible.renderMarks(this.model.getMarksByTypeByVersionedVerseId());
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                this.view.bible.enableNoteDeletion(noteId);
                console.error(error);
            });
    }

    _updateMarkingControlDisplay = () => {
        if (!this.hasAuthenticatedUser || this.model.getSelection().size === 0) {
            this.view.control.close();
            return;
        }
        const selectedMarks = this.model.getSelectedMarks();
        this.view.control.render([...selectedMarks.highlights.keys()]);
    };

    /**
     * @param {string} selectedColorCode
     * @param {MarksByType} selectedMarks
     * @private
     */
    _removeHighlights = (selectedColorCode, selectedMarks) => {
        let selectedHighlightedVerses = [];

        selectedMarks.highlights.get(selectedColorCode).forEach(mark => {
            mark.markedVerses.forEach(markedVerse => {
                if (this.model.getSelection().has(markedVerse.verse.toVersionedId())) {
                    selectedHighlightedVerses.push(markedVerse);
                }
            });
        });

        this.client.deleteHighlights(selectedHighlightedVerses.map(markedVerse => markedVerse.id)).then(response => {
            selectedMarks.highlights.get(selectedColorCode).forEach(mark => {
                mark.markedVerses.forEach((markedVerse, versionedVerseId) => {
                    if (this.model.getSelection().has(versionedVerseId)) {
                        this.model.deleteHighlightedVerseById(mark.id, markedVerse.id);
                    }
                });
            });

            this.view.bible.renderMarks(this.model.getMarksByTypeByVersionedVerseId());
            this.model.clearSelection();
            this.view.bible.clearSelection();
            this._updateMarkingControlDisplay();
        });
    }

    /**
     * @param {string} selectedColorCode
     * @param {MarksByType} selectedMarks
     * @private
     */
    _replaceHighlights = (selectedColorCode, selectedMarks) => {
        let selectedHighlightedVerses = [];

        selectedMarks.highlights.forEach(marks => {
            marks.forEach(mark => {
                mark.markedVerses.forEach(markedVerse => {
                    if (this.model.getSelection().has(markedVerse.verse.toVersionedId())) {
                        selectedHighlightedVerses.push(markedVerse);
                    }
                });
            });
        });

        this.client.deleteHighlights(selectedHighlightedVerses.map(markedVerse => markedVerse.id)).then(response => {
            selectedMarks.highlights.forEach(marks => {
                marks.forEach(mark => {
                    mark.markedVerses.forEach((markedVerse, versionedVerseId) => {
                        if (this.model.getSelection().has(versionedVerseId)) {
                            this.model.deleteHighlightedVerseById(mark.id, markedVerse.id);
                        }
                    });
                });
            });

            this._saveHighlight(selectedColorCode);
        });
    }

    _saveHighlight = colorCode => {
        const markedVerses = [...this.model.getSelection().values()].map(v => MarkedVerse.fromVersionedVerseId(v));
        const mark = Mark.factory(colorCode, null, markedVerses);

        this._saveMark(mark)
            .then(_ => {
                this.view.bible.renderMarks(this.model.getMarksByTypeByVersionedVerseId());
                this.model.clearSelection();
                this.view.bible.clearSelection();
                this._updateMarkingControlDisplay();
            });
    }

    /**
     * @param {Mark} mark
     * @private
     */
    _saveMark = mark => {
        const payload = {
            mark,
            "location": {
                versionId: this.model.versionId,
                bookId: this.model.bookId,
                chapterId: this.model.chapterId,
            }
        }

        return this.client.postMark(payload)
            .then(response => {
                this.model.addMark(Mark.fromMarkResponse(response));
            }).catch(error => {
                this.view.notifier.notifyError(error.message);
                console.error(error);
            });
    }
}