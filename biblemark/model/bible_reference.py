from biblemark.model.bible_verse import BibleVerse
from biblemark.model.bible_verse_interval import BibleVerseInterval


class BibleReference:

    def __init__(self, verses: [BibleVerse]):
        if len(verses) == 0:
            raise ValueError("Bible reference without verses")

        self.verses = verses
        self.intervals = []

        left = None
        previous = None

        for verse in verses:
            current = verse

            if left is None:
                left = current
                previous = current
            else:
                if not previous.is_next_verse_sibling(current):
                    self.intervals.append(BibleVerseInterval(left, right=previous))
                    left = current
                previous = current

        self.intervals.append(BibleVerseInterval(left, right=previous))

    def __str__(self) -> str:
        return f"BibleReference(intervals=${self.intervals})"

    def __repr__(self) -> str:
        return f"BibleReference(intervals=${self.intervals!r})"
