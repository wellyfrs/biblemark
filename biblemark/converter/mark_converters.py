from typing import List

from biblemark.model.bible_reference_formatter import BibleReferenceFormatter
from biblemark.model.mark import Mark


def build_mark_creation_response(request: dict, mark: Mark) -> dict:
    mark.marked_verses = list(filter(
        lambda ref: ref.verse.version.get_internal_id() == request["location"]["versionId"]
                    and ref.verse.book.value.id == request["location"]["bookId"]
                    and ref.verse.chapter_id == request["location"]["chapterId"],
        mark.marked_verses
    ))
    return serialize_mark(mark)


def serialize_enriched_mark(mark: Mark, passages: List[dict]) -> dict:
    serialized_mark = serialize_mark(mark)
    serialized_mark["passages"] = passages
    return serialized_mark


def serialize_mark(mark: Mark) -> dict:
    return {
        "id": str(mark.entity_id),
        "color": mark.color,
        "note": mark.note,
        "reference": BibleReferenceFormatter.format(mark.to_reference()),
        "markedVerses": list(map(lambda marked_verse: {
            "id": str(marked_verse.entity_id),
            "verse": {
                "versionId": marked_verse.verse.version.get_internal_id(),
                "bookId": marked_verse.verse.book.value.id,
                "chapterId": marked_verse.verse.chapter_id,
                "verseNumber": marked_verse.verse.verse_number,
            },
        }, mark.marked_verses)),
        "marked": mark.marked,
    }
