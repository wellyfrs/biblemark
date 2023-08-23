from biblemark.model.bible_verse import BibleVerse
from biblemark.model.bible_version_structure import BibleVersionStructure


class BibleVerseInterval:

    def __init__(self, left: BibleVerse, right: BibleVerse):
        """
        Represents an interval of Biblical verses.

        :param  left: a, start
        :param right: b, end
        """
        if not isinstance(left, BibleVerse):
            raise ValueError("Left verse must be an instance of BibleVerse")

        if not isinstance(right, BibleVerse):
            raise ValueError("Right verse must be an instance of BibleVerse")

        if left.version != right.version:
            raise ValueError("Left and right verses must be from the same version")

        if left > right:
            raise ValueError("Left verse must be before or equal to the right verse")

        self.left = left
        self.right = right

    def is_degenerated(self) -> bool:
        """
        Returns whether the interval is degenerated or not.
        An interval [a, b] is degenerated if a = b, in this case, left = right.

        :return: True if degenerated, False otherwise.
        """
        return self.left == self.right

    def starts_at_chapter_beginning(self) -> bool:
        return self.left.verse_number == 1

    def ends_at_chapter_ending(self, structure) -> bool:
        return self.right.verse_number == structure.get(self.right.book).verses[self.right.chapter_id]

    def is_in_same_book(self) -> bool:
        return self.left.book == self.right.book

    def is_in_same_chapter(self) -> bool:
        return self.is_in_same_book() and \
            self.left.chapter_id == self.right.chapter_id

    def is_partial_chapter(self, structure) -> bool:
        return self.is_in_same_chapter() and \
            not (self.starts_at_chapter_beginning() and self.ends_at_chapter_ending(structure))

    def is_full_chapter(self, structure: BibleVersionStructure) -> bool:
        return self.is_in_same_chapter() and \
            self.starts_at_chapter_beginning() and \
            self.ends_at_chapter_ending(structure)

    def is_cross_full_chapter_interval(self, structure: BibleVersionStructure) -> bool:
        return not self.is_in_same_chapter() and \
            self.starts_at_chapter_beginning() and \
            self.ends_at_chapter_ending(structure)

    def is_cross_full_to_partial_chapter_interval(self, structure: BibleVersionStructure) -> bool:
        return not self.is_in_same_chapter() and \
            self.starts_at_chapter_beginning() and \
            not self.ends_at_chapter_ending(structure)

    def is_cross_partial_to_full_chapter_interval(self, structure: BibleVersionStructure) -> bool:
        return not self.is_in_same_chapter() and \
            not self.starts_at_chapter_beginning() and \
            self.ends_at_chapter_ending(structure)

    def to_id(self) -> str:
        if self.is_degenerated():
            return self.left.to_verse_id()
        return f"{self.left.to_verse_id()}-{self.right.to_verse_id()}"

    def __eq__(self, other) -> bool:
        return self.left == other.left and self.right == other.right

    def __lt__(self, other) -> bool:
        return self.left < other.left

    def __gt__(self, other) -> bool:
        return self.left > other.left

    def __str__(self) -> str:
        return f"BibleVerseInterval(left={self.left}, right={self.right})"

    def __repr__(self) -> str:
        return f"BibleVerseInterval(left={self.left!r}, right={self.right!r})"
