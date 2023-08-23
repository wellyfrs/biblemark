from sqlite3 import Row
from typing import Optional

from werkzeug.security import generate_password_hash

from biblemark.config.db import get_db
from biblemark.model.user import User


def save_user(user: User) -> User:
    db = get_db()

    user.entity_id = db.execute(
        "INSERT INTO user (username, display_name, password) VALUES (?, ?, ?)",
        (user.username, user.name, generate_password_hash(user.password)),
    ).lastrowid

    db.commit()

    return user


def fetch_user_by_id(user_id: int) -> Optional[User]:
    return convert_row(get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone())


def fetch_user_by_username(username: str) -> Optional[User]:
    return convert_row(get_db().execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone())


def convert_row(row: Row) -> Optional[User]:
    if row:
        try:
            return User(
                entity_id=row["id"],
                username=row["username"],
                name=row["display_name"],
                password=row["password"],
                created=row["created"],
            )
        except KeyError:
            return None
    return None
