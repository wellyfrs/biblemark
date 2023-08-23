from biblemark.exceptions.user_http_exceptions import UsernameUnavailableError
from biblemark.model.user import User
from biblemark.repository.user_repository import fetch_user_by_username, save_user


def register_user(user: User) -> User:
    existing = fetch_user_by_username(user.username)

    if existing is not None:
        raise UsernameUnavailableError(f"Username [{user.username}] has already been taken")
    else:
        return save_user(user)
