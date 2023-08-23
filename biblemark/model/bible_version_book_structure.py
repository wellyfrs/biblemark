from dataclasses import dataclass

from biblemark.model.bible_book import BibleBook


@dataclass(frozen=True)
class BibleVersionBookStructure:
    book: BibleBook
    order: int
    chapters: int
    verses: dict

    def __str__(self):
        return f"BibleVersionBookStructure(name={self.book.name}, order={self.order}, " \
               f"chapters={self.chapters} verses={self.verses}"

    def __repr__(self):
        return f"BibleVersionBookStructure(book={self.book!r}, order={self.order!r}, " \
               f"chapters={self.chapters!r}, verses={self.verses!r})"
