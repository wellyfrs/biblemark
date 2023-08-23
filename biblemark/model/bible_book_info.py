from dataclasses import dataclass


@dataclass(frozen=True)
class BibleBookInfo:
    id: str
    english_name: str

    def __post_init__(self):
        if not self.id:
            raise ValueError("The 'id' field cannot be empty")

        if not self.english_name:
            raise ValueError("The 'english_name' field cannot be empty")

    def __str__(self) -> str:
        return f"BibleBookInfo(id={self.id}, english_name='{self.english_name}')"

    def __repr__(self) -> str:
        return f"BibleBookInfo(id={self.id!r}, english_name='{self.english_name!r}')"
