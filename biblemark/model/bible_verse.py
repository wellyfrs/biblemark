from __future__ import annotations

from biblemark.model.bible_book import BibleBook
from biblemark.model.bible_version import Version


class BibleVerse:

    def __init__(self, version: Version, book: BibleBook, chapter_id: str, verse_number: int):
        if not isinstance(version, Version):
            raise ValueError("Invalid version")

        if not isinstance(book, BibleBook):
            raise ValueError("Invalid book")

        if not isinstance(chapter_id, str) or not chapter_id:
            raise ValueError("Invalid chapter")

        if int(verse_number) < 1:
            raise ValueError("Invalid verse")

        self.version = version
        self.book = book
        self.chapter_id = chapter_id
        self.verse_number = verse_number

    def to_verse_id(self) -> str:
        return f"{self.book.get_id()}.{self.chapter_id}.{self.verse_number}"

    def to_versioned_id(self) -> str:
        return f"{self.version.get_internal_id()}.{self.to_verse_id()}"

    def is_next_verse_sibling(self, other: BibleVerse) -> bool:
        return (
            other.version == self.version
            and other.book == self.book
            and other.chapter_id == self.chapter_id
            and int(other.verse_number) == int(self.verse_number) + 1
        )

    def __eq__(self, other: BibleVerse) -> bool:
        return (
            self.version == other.version
            and self.book == other.book
            and self.chapter_id == other.chapter_id
            and self.verse_number == other.verse_number
        )

    def __lt__(self, other) -> bool:
        if self.version != other.version:
            raise ValueError("Verse comparison between different versions")

        book = self.version.structure.get(self.book).order
        other_book = self.version.structure.get(other.book).order

        if book == other_book:
            if self.chapter_id == other.chapter_id:
                if self.verse_number == other.verse_number:
                    return False
                elif self.verse_number < other.verse_number:
                    return True
            elif self.chapter_id < other.chapter_id:
                return True
        elif book < other_book:
            return True
        return False

    def __str__(self) -> str:
        return f"BibleVerse({self.to_versioned_id()})"

    def __repr__(self) -> str:
        return f"BibleVerse({self.to_versioned_id()!r})"
