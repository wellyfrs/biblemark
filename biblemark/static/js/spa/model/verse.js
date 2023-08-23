const VERSE_ID_SEPARATOR = '.';

export default class Verse {

    /**
     * @param {string} versionId
     * @param {string} bookId
     * @param {string} chapterId
     * @param {string} verseNumber
     */
    constructor(versionId, bookId, chapterId, verseNumber) {
        this.versionId = versionId;
        this.bookId = bookId;
        this.chapterId = chapterId;
        this.verseNumber = verseNumber;
    }

    /**
     * @param {VersionedVerseId} versionedVerseId
     * @returns {Verse}
     */
    static fromVersionedVerseId(versionedVerseId) {
        const parsed = Verse.parseVersionedVerseId(versionedVerseId);
        return new Verse(parsed.versionId, parsed.bookId, parsed.chapterId, parsed.verseNumber);
    }

    /**
     * @param {VersionedVerseId} versionedVerseId
     * @returns {{versionId: string, bookId: string, chapterId: string, verseNumber: number}}
     */
    static parseVersionedVerseId = (versionedVerseId) => {
        const parts = versionedVerseId.split(VERSE_ID_SEPARATOR);

        if (parts.length !== 4) {
            console.error('Invalid input format');
            return null;
        }

        let [versionId, bookId, chapterId, verseNumber] = parts;

        if (!versionId || !bookId || !chapterId || !verseNumber) {
            console.error('All parts of the versioned verse ID must be non-empty');
            return null;
        }

        if (!/^\d+$/.test(verseNumber)) {
            console.error('Verse number should be a positive integer');
            return null;
        }

        verseNumber = +verseNumber;

        return { versionId, bookId, chapterId, verseNumber };
    }

    /**
     * Text representation for book ID, chapter number, and verse number, in that order.
     *
     * @typedef VerseId
     * @type {string}
     */

    /**
     * Generates text representation for the unique combination of
     * book, chapter, and verse, **without version**.
     * @returns {VerseId}
     */
    toVerseId = () => [this.bookId, this.chapterId, this.verseNumber].join(VERSE_ID_SEPARATOR);

    /**
     * Extends the {@link VerseId}, prepending version ID.
     *
     * @typedef VersionedVerseId
     * @type {string}
     */

    /**
     * Generates text representation for the unique combination of
     * version, book, chapter, and verse number.
     * @returns {VersionedVerseId}
     */
    toVersionedId = () => [this.versionId, this.bookId, this.chapterId, this.verseNumber].join(VERSE_ID_SEPARATOR);

    static generateVersionedId = (versionId, verseId) => `${versionId}.${verseId}`;
}