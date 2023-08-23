from datetime import datetime
from sqlite3 import Row
from typing import Optional, List

from biblemark.config.db import get_db
from biblemark.model.bible_version import Version
from biblemark.model.mark import Mark
from biblemark.model.marked_verse import MarkedVerse
from biblemark.model.user import User
from biblemark.model.bible_book import parse_book


def count_highlights_by_user(user: User) -> int:
    return get_db().execute(
        "SELECT count(*)"
        "  FROM mark m"
        " WHERE m.user_id = ?"
        "   AND m.color IS NOT NULL ",
        (user.entity_id,)
    ).fetchone()[0]


def count_notes_by_user(user: User) -> int:
    return get_db().execute(
        "SELECT count(*)"
        "  FROM mark m"
        " WHERE m.user_id = ?"
        "   AND m.note IS NOT NULL ",
        (user.entity_id,)
    ).fetchone()[0]


def fetch_mark_by_id(mark_id: str) -> Optional[Mark]:
    rows = get_db().execute(
        "SELECT m.*, m.id as mark_id, mv.*, mv.id as marked_verse_id, v.*, u.*"
        "  FROM mark m"
        "  JOIN marked_verse mv"
        "    ON mv.mark_id = m.id"
        "  JOIN version v"
        "    ON v.internal_id = mv.version_id"
        "  JOIN user u"
        "    ON u.id = m.user_id"
        " WHERE m.id = ?",
        (mark_id,)
    ).fetchall()
    converted = convert_rows(rows)
    return converted[0] if len(converted) != 0 else None


def fetch_paginated_highlights_by_user(user: User, limit: int, offset: int) -> List[Mark]:
    rows = get_db().execute(
        "SELECT m.*, m.id as mark_id, mv.*, mv.id as marked_verse_id, v.*, u.*"
        "  FROM mark m"
        "  JOIN marked_verse mv"
        "    ON mv.mark_id = m.id"
        "  JOIN version v"
        "    ON v.internal_id = mv.version_id"
        "  JOIN user u"
        "    ON u.id = m.user_id"
        " WHERE u.id = ?"
        "   AND m.color IS NOT NULL"
        "   AND m.id IN"
        "       (SELECT mark.id"
        "          FROM mark"
        "         WHERE mark.user_id = ?"
        "           AND mark.color IS NOT NULL"
        "         ORDER BY mark.marked DESC"
        "         LIMIT ?"
        "        OFFSET ?)"
        " ORDER BY m.marked DESC",
        (user.entity_id,
         user.entity_id,
         limit,
         offset,)
    ).fetchall()

    return convert_rows(rows)


def fetch_paginated_notes_by_user(user: User, limit: int, offset: int) -> List[Mark]:
    rows = get_db().execute(
        "SELECT m.*, m.id as mark_id, mv.*, mv.id as marked_verse_id, v.*, u.*"
        "  FROM mark m"
        "  JOIN marked_verse mv"
        "    ON mv.mark_id = m.id"
        "  JOIN version v"
        "    ON v.internal_id = mv.version_id"
        "  JOIN user u"
        "    ON u.id = m.user_id"
        " WHERE u.id = ?"
        "   AND m.note IS NOT NULL"
        "   AND mark_id IN"
        "       (SELECT mark.id"
        "          FROM mark"
        "         WHERE mark.user_id = ?"
        "           AND mark.note IS NOT NULL"
        "         ORDER BY mark.marked DESC"
        "         LIMIT ?"
        "        OFFSET ?)"
        " ORDER BY m.marked DESC",
        (user.entity_id,
         user.entity_id,
         limit,
         offset,)
    ).fetchall()

    return convert_rows(rows)


def fetch_visible_marks_by_user_and_chapter(user: User, version_id: str, book_id: str, chapter_id: str) -> List[Mark]:
    rows = get_db().execute(
        "SELECT m.*, m.id as mark_id, mv.*, mv.id as marked_verse_id, v.*, u.*"
        "  FROM mark m"
        "  JOIN marked_verse mv"
        "    ON mv.mark_id = m.id"
        "  JOIN version v"
        "    ON v.internal_id = mv.version_id"
        "  JOIN user u"
        "    ON u.id = m.user_id"
        " WHERE u.id = ?"
        "   AND mv.version_id = ?"
        "   AND mv.book_id = ?"
        "   AND mv.chapter_id = ?"
        "   AND mv.visibility IS TRUE",
        (user.entity_id,
         version_id,
         book_id,
         chapter_id,)
    ).fetchall()

    return convert_rows(rows)


def save_mark(mark: Mark) -> Mark:
    db = get_db()

    if mark.entity_id:
        db.execute(
            "UPDATE mark"
            "   SET color = ?, note = ?"
            " WHERE id = ?",
            (mark.color,
             mark.note,
             mark.entity_id,)
        )
    else:
        mark.marked = datetime.now()
        mark.entity_id = db.execute(
            "INSERT INTO mark (user_id, color, note, marked) "
            "VALUES (?, ?, ?, ?)",
            (mark.user.entity_id,
             mark.color,
             mark.note,
             mark.marked),
        ).lastrowid

        for marked_verse in mark.marked_verses:
            marked_verse.entity_id = db.execute(
                "INSERT INTO marked_verse (version_id, book_id, chapter_id, verse_number, visibility, mark_id) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (marked_verse.verse.version.get_internal_id(),
                 marked_verse.verse.book.get_id(),
                 marked_verse.verse.chapter_id,
                 marked_verse.verse.verse_number,
                 marked_verse.visibility, mark.entity_id),
            ).lastrowid

    db.commit()

    return mark


def delete_mark_by_id(mark_id: str):
    db = get_db()

    db.execute(
        "DELETE"
        "  FROM mark"
        " WHERE id = ?",
        (mark_id,)
    )

    db.commit()


def soft_delete_marked_verses_by_ids(marked_verse_ids: List[str]):
    db = get_db()

    db.execute(
        "UPDATE marked_verse"
        "   SET visibility = FALSE"
        " WHERE id IN (?)",
        (", ".join(marked_verse_ids),)
    )

    db.commit()


def soft_delete_all_highlights_at_verses(marked_verses: List[MarkedVerse]):
    db = get_db()

    for marked_verse in marked_verses:
        db.execute(
            "UPDATE marked_verse"
            "   SET visibility = FALSE"
            " WHERE version_id = ?"
            "   AND book_id = ?"
            "   AND chapter_id = ?"
            "   AND verse_number = ?"
            "   AND mark_id IN"
            "       (SELECT id"
            "          FROM mark"
            "         WHERE color IS NOT NULL)",
            (marked_verse.verse.version.get_internal_id(),
             marked_verse.verse.book.get_id(),
             marked_verse.verse.chapter_id,
             marked_verse.verse.verse_number,)
        )

    db.commit()


def convert_rows(rows: List[Row]) -> List[Mark]:
    marks = {}

    for row in rows:
        marked_verse = MarkedVerse.factory(
            entity_id=row["marked_verse_id"],
            version=Version(
                row["internal_id"],
                row["external_id"],
                row["lang"],
                row["name"],
                bool(row["disabled"])
            ),
            book_id=parse_book(row["book_id"]),
            chapter_id=row["chapter_id"],
            verse_number=row["verse_number"],
            visibility=bool(row["visibility"]),
        )

        if row["mark_id"] in marks:
            marks[row["mark_id"]].add_marked_verse(marked_verse)
        else:
            marks[row["mark_id"]] = Mark(
                entity_id=row["mark_id"],
                user=User(
                    entity_id=row["user_id"],
                    name=row["display_name"],
                    username=row["username"],
                    password=None  # do not expose password hash
                ),
                color=row["color"],
                note=row["note"],
                marked_verses=[marked_verse],
                marked=row["marked"]
            )

    return list(marks.values())
