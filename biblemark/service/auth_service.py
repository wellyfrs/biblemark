from flask import session
from werkzeug.security import check_password_hash

from biblemark.exceptions.user_http_exceptions import InvalidCredentialsError
from biblemark.repository.user_repository import fetch_user_by_username


def authenticate(username, password):
    persisted = fetch_user_by_username(username)

    if persisted is None or not check_password_hash(persisted.password, password):
        raise InvalidCredentialsError("Invalid credentials")

    session.clear()
    session["user_id"] = persisted.entity_id


def unauthenticate():
    session.clear()
