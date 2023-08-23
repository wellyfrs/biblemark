from biblemark.exceptions.mark_http_exceptions import InvalidMarkedVerse
from biblemark.model.bible_verse import BibleVerse
from biblemark.model.bible_version import Version


class MarkedVerse:

    def __init__(self, verse: BibleVerse, visibility: bool = True, entity_id=None):
        self.entity_id = entity_id
        self.verse = verse

        if not isinstance(visibility, bool):
            raise InvalidMarkedVerse("No boolean indicator of visibility assigned to mark reference")
        self.visibility = visibility

    @staticmethod
    def factory(version: Version, book_id, chapter_id, verse_number, visibility=True, entity_id=None):
        return MarkedVerse(BibleVerse(version, book_id, chapter_id, verse_number), visibility, entity_id)

    def __str__(self) -> str:
        return f"MarkedVerse(id={self.entity_id}, verse={self.verse}, visibility={self.visibility})"

    def __repr__(self) -> str:
        return f"MarkedVerse(id={self.entity_id!r}, verse={self.verse!r}, visibility={self.visibility!r})"
