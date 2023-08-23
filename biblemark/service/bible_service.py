from biblemark.exceptions.bible_http_exceptions import VersionNotFound, BookNotFound, ChapterNotFound
from biblemark.model.bible_version import Version
from biblemark.repository.bible_repository import fetch_supported_versions, fetch_supported_version
from biblemark.service.external_bible_api_service import fetch_books, fetch_chapters, fetch_chapter
from biblemark.utils.helpers import associate_by


def get_versions() -> [dict]:
    supported_versions = fetch_supported_versions()
    return list({"id": version.get_internal_id(), "name": version.name} for version in supported_versions)


def get_version(version_id) -> Version:
    result = fetch_supported_version(version_id)
    if result is None:
        raise VersionNotFound(f"Version {version_id} not found")
    return result


def get_books(version_id) -> [dict]:
    version = get_version(version_id)
    books = fetch_books(version.external_id)["data"]
    return list({"id": book["id"], "name": book["name"]} for book in books)


def get_chapters(version_id, book_id) -> [dict]:
    version = get_version(version_id)
    chapters = fetch_chapters(version.external_id, book_id)["data"]
    return list({"id": chapter["number"]} for chapter in chapters)


def get_chapter_content(version_id, book_id, chapter_id) -> dict:
    version = get_version(version_id)

    books = associate_by(fetch_books(version.external_id)["data"], "id")
    book = books.get(book_id.upper())

    if book is None:
        raise BookNotFound(f"Book {book_id} not found in version [{version.name}]")

    chapters = fetch_chapters(version.external_id, book["id"])["data"]
    chapters = associate_by(chapters, "number")
    chapter = chapters.get(str(chapter_id))

    if chapter is None:
        raise ChapterNotFound(
            f"Chapter {book['name']} {chapter_id} not found in version {version.name}."
        )

    return fetch_chapter(version.external_id, chapter["id"])["data"]
