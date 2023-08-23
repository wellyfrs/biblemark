import re


class User:
    USERNAME_REGEX = r"^[a-zA-Z0-9_]+$"

    def __init__(self, username, name, password, entity_id=None, created=None):
        if not re.match(User.USERNAME_REGEX, username):
            raise ValueError("Username must only contain letters, numbers, and underscores")

        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        self.username = username
        self.name = name
        self.password = password
        self.entity_id = entity_id
        self.created = created

    def __str__(self) -> str:
        return f"User(id={self.entity_id}, username={self.username}, name={self.name}, created={self.created})"

    def __repr__(self) -> str:
        return f"User(id={self.entity_id!r}, username={self.username!r}, name={self.name!r}, created={self.created!r})"
