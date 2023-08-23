import Verse from './verse.js';

export default class MarkedVerse {

    /**
     * @param {string} id
     * @param {Verse} verse
     */
    constructor(id, verse) {
        this.id = id;
        this.verse = verse;
    }

    /**
     * @param {string} id
     * @param {string} versionId
     * @param {string} bookId
     * @param {string} chapterId
     * @param {string} verseNumber
     * @returns {MarkedVerse}
     */
    static factory = (id, versionId, bookId, chapterId, verseNumber) =>
        new MarkedVerse(id, new Verse(versionId, bookId, chapterId, verseNumber));

    /**
     * @param {VersionedVerseId} versionedVerseId
     * @returns {MarkedVerse}
     */
    static fromVersionedVerseId = (versionedVerseId) =>
        new MarkedVerse(null, Verse.fromVersionedVerseId(versionedVerseId));
}