import MarkedVerse from "./markedVerse.js";

export default class Mark {

    /**
     * @param {string} id
     * @param {string} color
     * @param {string} note
     * @param {string} reference
     * @param {Map<VersionedVerseId, MarkedVerse>} markedVerses
     * @param {string} marked
     */
    constructor(id, color, note, reference, markedVerses, marked) {
        /**
         * @type {string}
         */
        this.id = id;

        /**
         * @type {string|null}
         */
        this.color = color ? String(color) : null;

        /**
         * @type {string|null}
         */
        this.note = note ? String(note) : null;

        /**
         * @type {string}
         */
        this.reference = reference;

        /**
         * @type {Map<VersionedVerseId, MarkedVerse>}
         */
        this.markedVerses = markedVerses;

        /**
         * @type {Date|null}
         */
        this.marked = marked ? new Date(marked) : null;
    }

    /**
     * @param {string} color
     * @param {string} note
     * @param {Map<VersionedVerseId, MarkedVerse>} markedVerses
     * @returns {Mark}
     */
    static factory = (color, note, markedVerses) =>
        new Mark(null, color, note, null, markedVerses, null);

    /**
     * @param {MarkResponseItem} markResponse
     * @returns {Mark}
     */
    static fromMarkResponse(markResponse) {
        return new Mark(
            markResponse.id,
            markResponse.color,
            markResponse.note,
            markResponse.reference,
            markResponse.
            markedVerses.reduce((map, markedVerseResponse) => {
                const markedVerse = MarkedVerse.factory(
                    markedVerseResponse.id,
                    markedVerseResponse.verse.versionId,
                    markedVerseResponse.verse.bookId,
                    markedVerseResponse.verse.chapterId,
                    markedVerseResponse.verse.verseNumber,
                )
                return map.set(markedVerse.verse.toVersionedId(), markedVerse);
            }, new Map()),
            markResponse.marked,
        );
    }
}