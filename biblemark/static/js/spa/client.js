export default class Client {

    /**
     * @param {string} baseUrl
     */
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * @typedef User
     * @type {object}
     * @property {number} id
     * @property {string} username
     * @property {string} name
     * @property {string} created
     */

    /**
     * @typedef UserResponse
     * @type {object}
     * @property {User} user
     */

    /**
     * @returns {Promise<UserResponse>}
     */
    fetchMe = () =>
        this._request(new URL('/api/me', this.baseUrl));

    /**
     * @typedef VersionsResponse
     * @type {object}
     * @property {[VersionResponseItem]} versions
     */

    /**
     * @typedef VersionResponseItem
     * @type {object}
     * @property {string} id
     * @property {string} name
     */

    /**
     * @returns {Promise<VersionsResponse>}
     */
    fetchVersions = () =>
        this._request(new URL('/api/versions', this.baseUrl));

    /**
     * @typedef BooksResponse
     * @type {object}
     * @property {[BookResponseItem]} books
     */

    /**
     * @typedef BookResponseItem
     * @type {object}
     * @property {string} id
     * @property {string} name
     */

    /**
     * @param {string} versionId
     * @returns {Promise<BooksResponse>}
     */
    fetchBooks = (versionId) =>
        this._request(new URL(`/api/versions/${versionId}/books`, this.baseUrl));

    /**
     * @typedef ChaptersResponse
     * @type {object}
     * @property {[ChapterResponseItem]} chapters
     */

    /**
     * @typedef ChapterResponseItem
     * @type {object}
     * @property {string} id
     */

    /**
     * @param {string} versionId
     * @param {string} bookId
     * @returns {Promise<ChaptersResponse>}
     */
    fetchChapters = (versionId, bookId) =>
        this._request(new URL(`/api/versions/${versionId}/books/${bookId}/chapters`, this.baseUrl));

    /**
     * @typedef ChapterResponse
     * @type {object}
     * @property {Chapter} chapter
     * @property {ChapterLinks} _links
     */

    /**
     * @typedef Chapter
     * @type {object}
     * @property {string} versionId
     * @property {string} bookId
     * @property {string} chapterId
     * @property {string} reference
     * @property {string} content
     */

    /**
     * @typedef ChapterLinks
     * @type {object}
     * @property {ChapterLink} prev
     * @property {ChapterLink} self
     * @property {ChapterLink} next
     */

    /**
     * @typedef ChapterLink
     * @type {object}
     * @property {string} versionId
     * @property {string} bookId
     * @property {string} chapterId
     * @property {string} href
     */

    /**
     * @param {string} versionId
     * @param {string} bookId
     * @param {string} chapterId
     * @returns {Promise<ChapterResponse>}
     */
    fetchChapter = (versionId, bookId, chapterId) =>
        this._request(new URL(`/api/versions/${versionId}/books/${bookId}/chapters/${chapterId}`, this.baseUrl));

    /**
     * @typedef MarksResponse
     * @type {object}
     * @property {[MarkResponseItem]} marks
     */

    /**
     * @typedef MarkResponseItem
     * @type {object}
     * @property {string} id
     * @property {string} color
     * @property {string} note
     * @property {string} reference
     * @property {[MarkedVerseResponse]} markedVerses
     * @property {string} marked
     */

    /**
     * @typedef MarkedVerseResponse
     * @type {object}
     * @property {string} id
     * @property {MarkedVerseResponseVerse} verse
     */

    /**
     * @typedef MarkedVerseResponseVerse
     * @type {object}
     * @property {string} versionId
     * @property {string} bookId
     * @property {string} chapterId
     * @property {string} verseNumber
     */

    /**
     * @param {string} versionId
     * @param {string} bookId
     * @param {string} chapterId
     * @returns {Promise<MarksResponse>}
     */
    fetchChapterMarks = (versionId, bookId, chapterId) =>
        this._request(new URL(`/api/marks/versions/${versionId}/books/${bookId}/chapters/${chapterId}`, this.baseUrl));

    /**
     * @param {Mark} mark
     * @returns {Promise<*>}
     */
    postMark = mark =>
        this._request(new URL('/api/marks', this.baseUrl), HTTPMethod.POST, mark);

    /**
     * @param {[string]} markedVerseIds
     * @returns {Promise<*>}
     */
    deleteHighlights = (markedVerseIds = []) => {
        const url = new URL('/api/marks/highlights', this.baseUrl);
        if (markedVerseIds.length > 0) {
            url.searchParams.append('markedVerses', markedVerseIds.join());
        }
        return this._request(url, HTTPMethod.DELETE);
    }

    /**
     * @param {string} markId
     * @returns {Promise<*>}
     */
    deleteMark = markId =>
        this._request(new URL(`/api/marks/${markId}`, this.baseUrl), HTTPMethod.DELETE);

    /**
     * @param {Mark} markId
     * @param {object} body
     * @returns {Promise<*>}
     */
    patchMark = (markId, body) =>
        this._request(new URL(`/api/marks/${markId}`, this.baseUrl), HTTPMethod.PATCH, body)

    /**
     * @param {URL} url
     * @param {HTTPMethod} method
     * @param {object} body
     * @returns {Promise<any>}
     * @private
     */
    _request(url = new URL(this.baseUrl), method = HTTPMethod.GET, body = null) {
        let init = {
            mode: 'same-origin',
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if ([HTTPMethod.POST, HTTPMethod.PATCH].includes(method)) {
            init.body = JSON.stringify(body);
        }

        return fetch(url, init).then(response => {
            return response.json().then(data => {
                if (!response.ok) {
                    throw new Error(data['description']);
                }
                return data;
            });
        });
    }
}

const HTTPMethod = {
    GET: 'GET',
    POST: 'POST',
    PUT: 'PUT',
    PATCH: 'PATCH',
    DELETE: 'DELETE'
}