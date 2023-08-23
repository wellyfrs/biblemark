from sqlite3 import Row
from typing import Optional, List

from biblemark.config.db import get_db
from biblemark.model.bible_version import Version


def fetch_supported_versions() -> [Optional[Version]]:
    rows = get_db().execute(
        "SELECT *"
        "  FROM version v"
        " WHERE v.disabled IS FALSE"
        " ORDER BY v.internal_id",
    ).fetchall()

    return convert_version_rows(rows)


def fetch_supported_version(internal_id) -> Optional[Version]:
    row = get_db().execute(
        "SELECT *"
        "  FROM version v"
        " WHERE v.internal_id = ?"
        "   AND v.disabled IS FALSE ",
        (internal_id,)
    ).fetchone()

    return convert_version_row(row)


def convert_version_rows(rows) -> List[Optional[Version]]:
    return [convert_version_row(row) for row in rows]


def convert_version_row(row: Row) -> Optional[Version]:
    if row is None:
        return None
    return Version(
        row["internal_id"],
        row["external_id"],
        row["lang"],
        row["name"],
        bool(row["disabled"]),
    )
