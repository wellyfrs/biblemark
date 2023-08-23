from biblemark.model.bible_version_structure import COMMON_PROTESTANT_STRUCTURE, BibleVersionStructure


class Version:

    def __init__(self,
                 internal_id: str,
                 external_id: str,
                 lang: str,
                 name: str,
                 disabled: bool,
                 structure=COMMON_PROTESTANT_STRUCTURE
                 ):
        if not isinstance(internal_id, str) or not internal_id:
            raise ValueError("Internal ID must be a non-empty string")

        if not isinstance(external_id, str) or not external_id:
            raise ValueError("External ID must be a non-empty string")

        if not isinstance(lang, str) or not lang:
            raise ValueError("Language must be a non-empty string")

        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")

        if not isinstance(disabled, bool):
            raise ValueError("Disabled flag must be a boolean value")

        if not isinstance(structure, BibleVersionStructure):
            raise ValueError("Version structure must be an instance of BibleVersionStructure")

        self.internal_id = internal_id
        self.external_id = external_id
        self.lang = lang
        self.name = name
        self.disabled = disabled
        self.structure = structure

    def get_internal_id(self) -> str:
        return self.internal_id

    def __eq__(self, other) -> bool:
        return self.internal_id == other.internal_id

    def __str__(self) -> str:
        return self.internal_id
