import re
from typing import List

from biblemark.model.bible_reference import BibleReference
from biblemark.model.marked_verse import MarkedVerse
from biblemark.model.user import User


class Mark:
    COLOR_CODE_FORMAT = r"^#?[0-9a-f]{6}$"
    MAX_NOTE_LENGTH = 1024

    def __init__(self,
                 user: User,
                 color: str,
                 note: str,
                 marked_verses: List[MarkedVerse],
                 entity_id=None,
                 marked=None
                 ):
        self.entity_id = entity_id

        if user is None:
            raise ValueError("Invalid user for mark")

        if color is not None:
            if not bool(re.match(self.COLOR_CODE_FORMAT, color, re.IGNORECASE)):
                raise ValueError("Invalid color for mark")

        if note is not None:
            if not isinstance(note, str) or (len(note.strip()) == 0):
                raise ValueError("Invalid note text for mark")
            if len(note) > self.MAX_NOTE_LENGTH:
                raise ValueError("Too long note text for mark")

        if len(marked_verses) == 0:
            raise ValueError("Mark without marked verses")

        self.user = user
        self.color = color
        self.note = note
        self.marked_verses = marked_verses
        self.marked = marked

    def add_marked_verse(self, marked_verse: MarkedVerse) -> None:
        self.marked_verses.append(marked_verse)

    def to_reference(self) -> BibleReference:
        return BibleReference([v.verse for v in self.marked_verses])

    def __str__(self) -> str:
        return f"Mark(id={self.entity_id}, user={self.user.username}, marked={self.marked}, " + \
               (f"color={self.color}, " if self.color else "") + \
               (f"note={self.note[:20]}..., " if self.note else "") + \
               f"verses={self.marked_verses})"

    def __repr__(self) -> str:
        return f"Mark(id={self.entity_id!r}, user={self.user!r}, marked={self.marked!r}, " + \
               (f"color={self.color!r}, " if self.color else "None") + \
               (f"note={self.note!r}, " if self.note else "None") + \
               f"verses={self.marked_verses!r})"
