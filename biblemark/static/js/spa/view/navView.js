export default class NavView {

    constructor() {
        this.version = document.getElementById('version');
        this.book = document.getElementById('book');
        this.chapter = document.getElementById('chapter');
        this.prev = document.getElementById('prev');
        this.next = document.getElementById('next');
    }

    // rendering

    /**
     * @param {[VersionResponseItem]} versions
     * @param {string} selectedVersionId
     */
    renderVersionSelectElement(versions, selectedVersionId) {
        this.version.innerHTML = '';
        versions.forEach((versionResponse, key) => {
            this.version[key] = new Option(
                versionResponse.name,
                versionResponse.id,
                false,
                versionResponse.id === selectedVersionId
            );
        });
    }

    /**
     * @param {[BookResponseItem]} books
     * @param {string} selectedBookId
     */
    renderBookSelectElement(books, selectedBookId) {
        this.book.innerHTML = '';
        books.forEach((bookResponse, key) => {
            this.book[key] = new Option(
                bookResponse.name,
                bookResponse.id,
                false,
                bookResponse.id === selectedBookId
            );
        });
    }

    /**
     * @param {[ChapterResponseItem]} chapters
     * @param {string} selectedChapterId
     */
    renderChapterSelectElement = (chapters, selectedChapterId) => {
        this.chapter.innerHTML = '';
        chapters.forEach((chapterResponse, key) => {
            this.chapter[key] = new Option(
                chapterResponse.id,
                chapterResponse.id,
                false,
                chapterResponse.id === selectedChapterId
            );
        });
    }

    // user feedback

    disableAllSelectElements = () =>
        [this.version, this.book, this.chapter, this.prev, this.next].forEach(i => i.disabled = true);

    enableAllSelectElements = () =>
        [this.version, this.book, this.chapter, this.prev, this.next].forEach(i => i.disabled = false);

    // bindings

    /**
     * @param {changeVersionHandlerCallback} handler
     */
    bindChangeVersion = handler =>
        this.version.addEventListener('change', event => handler(event.target.value));

    /**
     * @param {changeBookHandlerCallback} handler
     */
    bindChangeBook = handler =>
        this.book.addEventListener('change', event => handler(event.target.value));

    /**
     * @param {changeChapterHandlerCallback} handler
     */
    bindChangeChapter = handler =>
        this.chapter.addEventListener('change', event => handler(event.target.value));

    /**
     * @param {navPrevHandlerCallback} handler
     */
    bindNavPrev = handler =>
        this.prev.addEventListener('click', () => handler());

    /**
     * @param {navNextHandlerCallback} handler
     */
    bindNavNext = handler =>
        this.next.addEventListener('click', () => handler());
}