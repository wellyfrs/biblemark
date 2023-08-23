from biblemark.model.bible_reference import BibleReference
from biblemark.model.bible_verse_interval import BibleVerseInterval


class BibleReferenceFormatter:
    """
    Formatter for printing Bible reference objects.
    """

    DEFAULT_CROSS_BOOK_DELIMITER = " — "
    DEFAULT_CROSS_CHAPTER_DELIMITER = "—"
    DEFAULT_CROSS_VERSE_DELIMITER = "-"

    DEFAULT_GROUP_SEPARATOR = ";"
    DEFAULT_VERSE_GROUP_SEPARATOR = ","
    DEFAULT_CHAPTER_VERSE_SEPARATOR = ":"

    @staticmethod
    def format(
            bible_reference: BibleReference,
            gs: str = DEFAULT_GROUP_SEPARATOR,
            vgs: str = DEFAULT_VERSE_GROUP_SEPARATOR,
            cbd: str = DEFAULT_CROSS_BOOK_DELIMITER,
            ccd: str = DEFAULT_CROSS_CHAPTER_DELIMITER,
            cvd: str = DEFAULT_CROSS_VERSE_DELIMITER,
            cvs: str = DEFAULT_CHAPTER_VERSE_SEPARATOR,
    ) -> str:
        """
        Formats a BibleReference object.

        :param bible_reference: BibleReference object
        :param gs: group separator (default: ";")
        :param vgs: verse group separator (default: ",")
        :param cbd: cross-book delimiter (default: " — "
        :param ccd: cross-chapter delimiter (default: "—")
        :param cvd: cross-verse delimiter (default: "-")
        :param cvs: chapter-verse separator (default: ":")
        :return:
        """
        groups = []
        previous = None

        bible_reference.intervals.sort()

        for current in bible_reference.intervals:
            if previous is None:
                groups.append(BibleReferenceFormatter.format_interval(current))
                previous = current
                continue

            if current.left.version == previous.right.version:
                if current.left.book == previous.right.book:
                    if current.left.chapter_id == previous.right.chapter_id:
                        groups.append(vgs)
                        if current.is_degenerated():
                            groups.append(str(current.left.verse_number))
                        else:
                            groups.append(f"{current.left.verse_number}{cvd}{current.right.verse_number}")
                    else:
                        groups.append(gs)
                        groups.append(BibleReferenceFormatter.format_numbering(current, ccd, cvd, cvs))
                else:
                    groups.append(gs)
                    groups.append(BibleReferenceFormatter.format_interval(current, cbd, ccd, cvd, cvs))
            else:
                groups.append(f" ({previous.right.version})")
                groups.append(gs)
                groups.append(BibleReferenceFormatter.format_interval(current, cbd, ccd, cvd, cvs))
            previous = current

        return "".join(groups)

    @staticmethod
    def format_interval(
            i: BibleVerseInterval,
            cbd: str = DEFAULT_CROSS_BOOK_DELIMITER,
            ccd: str = DEFAULT_CROSS_CHAPTER_DELIMITER,
            cvd: str = DEFAULT_CROSS_VERSE_DELIMITER,
            cvs: str = DEFAULT_CHAPTER_VERSE_SEPARATOR,
    ) -> str:
        """
        Formats a BibleVerseInterval object.

        :param i: BibleVerseInterval object
        :param cbd: cross-book delimiter (default: " — "
        :param ccd: cross-chapter delimiter (default: "—")
        :param cvd: cross-verse delimiter (default: "-")
        :param cvs: chapter-verse separator (default: ":")
        :return: formatted string
        """
        structure = i.left.version.structure

        if i.is_in_same_book():
            book = structure.get(i.left.book).book.value.english_name
            numbering = BibleReferenceFormatter.format_numbering(i, ccd, cvd, cvs)

            return f"{book} {numbering}"
        else:
            left_book = structure.get(i.left.book).book.value.english_name
            left = f"{left_book} {i.left.chapter_id}{cvs}{i.left.verse_number}"

            right_book = structure.get(i.right.book).book.value.english_name
            right = f"{right_book} {i.right.chapter_id}{cvs}{i.right.verse_number}"

            return f"{left}{cbd}{right}"

    @staticmethod
    def format_numbering(
            i: BibleVerseInterval,
            ccd: str = DEFAULT_CROSS_CHAPTER_DELIMITER,
            cvd: str = DEFAULT_CROSS_VERSE_DELIMITER,
            cvs: str = DEFAULT_CHAPTER_VERSE_SEPARATOR,
    ) -> str:
        """
        Formats both chapter and verse numbering of a verse range.

        :param i: BibleVerseInterval object
        :param ccd: cross-chapter delimiter (default: "—")
        :param cvd: cross-verse delimiter (default: "-")
        :param cvs: chapter-verse separator (default: ":")
        :return: formatted string
        """
        structure = i.left.version.structure

        # intervals in the same chapter

        if i.is_degenerated():
            # e.g. 1:1 -> verse 1 of chapter 1
            return f"{i.left.chapter_id}{cvs}{i.left.verse_number}"

        if i.is_partial_chapter(structure):
            # e.g. 1:1-2 -> verse 1 and 2 of chapter 1
            return f"{i.left.chapter_id}{cvs}{i.left.verse_number}{cvd}{i.right.verse_number}"

        if i.is_full_chapter(structure):
            # e.g. 1 -> full chapter 1
            return f"{i.left.chapter_id}"

        # intervals across chapters

        if i.is_cross_full_chapter_interval(structure):
            # e.g. 1—2 -> full chapters 1 and 2
            return f"{i.left.chapter_id}{ccd}{i.right.chapter_id}"

        if i.is_cross_full_to_partial_chapter_interval(structure):
            # e.g. "1—2:1" -> full chapter 1, and verse 1 of chapter 2
            return f"{i.left.chapter_id}{ccd}{i.right.chapter_id}{cvs}{i.right.verse_number}"

        if i.is_cross_partial_to_full_chapter_interval(structure):
            # e.g. "1:2—2" -> chapter 1 from verse 2, and full chapter 2
            return f"{i.left.chapter_id}{cvs}{i.left.verse_number}{ccd}{i.right.chapter_id}"

        # default fallback
        # e.g. "1:2—2:1" -> chapter 1 from verse 2, and verse 1 of chapter 2
        return f"{i.left.chapter_id}{cvs}{i.left.verse_number}{ccd}{i.right.chapter_id}{cvs}{i.right.verse_number}"
