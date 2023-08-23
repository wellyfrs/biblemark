from concurrent.futures import ThreadPoolExecutor
from typing import List

from flask import g, abort

from biblemark.exceptions.mark_http_exceptions import MarkNotFound
from biblemark.model.bible_book import parse_book
from biblemark.model.bible_verse_interval import BibleVerseInterval
from biblemark.model.mark import Mark
from biblemark.model.marked_verse import MarkedVerse
from biblemark.model.user import User
from biblemark.repository.mark_repository import fetch_paginated_highlights_by_user, fetch_paginated_notes_by_user, \
    fetch_visible_marks_by_user_and_chapter, \
    save_mark, delete_mark_by_id, fetch_mark_by_id, soft_delete_all_highlights_at_verses
from biblemark.service.bible_service import get_version
from biblemark.service.external_bible_api_service import fetch_passages


def get_marks_by_user_and_chapter(user: User, version_id: str, book_id: str, chapter_id: str) -> List[Mark]:
    version = get_version(version_id)
    return fetch_visible_marks_by_user_and_chapter(user, version.get_internal_id(), book_id, chapter_id)


def get_highlights_by_user(user: User, page_number: int = 0, page_size: int = 30) -> List[dict]:
    offset = page_number * page_size
    marks = fetch_paginated_highlights_by_user(user, page_size, offset)
    return enrich_marks_in_parallel(marks)


def get_notes_by_user(user: User, page_number: int = 0, page_size: int = 30) -> List[dict]:
    offset = page_number * page_size
    marks = fetch_paginated_notes_by_user(user, page_size, offset)
    return enrich_marks_in_parallel(marks)


def enrich_marks_in_parallel(marks: List[Mark]) -> List[dict]:
    with ThreadPoolExecutor() as executor:
        enriched = list(executor.map(enrich_mark, marks))

    return enriched


def enrich_mark(mark: Mark) -> dict:
    passages = [get_passage(interval) for interval in mark.to_reference().intervals]

    return {
        "mark": mark,
        "passages": passages,
    }


def get_passage(verse_interval: BibleVerseInterval) -> dict:
    response = fetch_passages(
        version_id=verse_interval.left.version.external_id,
        passage_id=verse_interval.to_id(),
    )

    if response is None:
        abort(500)

    return {
        "link": f"/{verse_interval.left.book}/{verse_interval.left.chapter_id}",
        "content": response["data"]["content"],
        "reference": response["data"]["reference"]
    }


def create_mark(payload):
    versions = {}
    marked_verses = []

    for markedVerse in payload["mark"]["markedVerses"]:
        version_id = markedVerse["verse"]["versionId"]

        if version_id not in versions:
            versions[version_id] = get_version(version_id)

        marked_verses.append(
            MarkedVerse.factory(
                version=versions[version_id],
                book_id=parse_book(markedVerse["verse"]["bookId"]),
                chapter_id=markedVerse["verse"]["chapterId"],
                verse_number=markedVerse["verse"]["verseNumber"],
            )
        )

    mark = Mark(
        entity_id=None,
        user=User(
            entity_id=g.principal.entity_id,
            name=g.principal.name,
            username=g.principal.username,
            password=None,
        ),
        color=payload["mark"]["color"],
        note=payload["mark"]["note"],
        marked_verses=marked_verses,
    )

    if mark.color:
        soft_delete_all_highlights_at_verses(mark.marked_verses)

    return save_mark(mark)


def update_note_content_by(mark_id: str, mark_patch: dict):
    mark = fetch_mark_by_id(mark_id)

    if not mark or mark.user.entity_id != g.principal.entity_id:
        raise MarkNotFound("Mark not found")

    color = mark_patch.get("color")
    note = mark_patch.get("note")

    if color:
        mark.color = color

    if note:
        mark.note = note

    save_mark(mark)


def remove_mark(mark_id: str) -> Mark:
    mark = fetch_mark_by_id(mark_id)

    if not mark or mark.user.entity_id != g.principal.entity_id:
        raise MarkNotFound("Mark not found")

    delete_mark_by_id(mark_id)

    return mark
