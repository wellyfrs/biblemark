from flask import abort, render_template, Blueprint, current_app

from biblemark.exceptions.bible_http_exceptions import VersionNotFound, BookNotFound, ChapterNotFound
from biblemark.service.bible_service import get_chapter_content

bp = Blueprint("pages", __name__)


@bp.route("/")
@bp.route("/<version_id>/<book_id>/<chapter_id>")
def index(version_id=None, book_id=None, chapter_id=None):

    if version_id is None:
        version_id = current_app.config["DEFAULT_VERSION_ID"]

    if book_id is None:
        book_id = current_app.config["DEFAULT_BOOK_ID"]

    if chapter_id is None:
        chapter_id = current_app.config["DEFAULT_CHAPTER_ID"]

    try:
        get_chapter_content(version_id, book_id, chapter_id)
    except (VersionNotFound, BookNotFound, ChapterNotFound):
        return abort(404)
    else:
        return render_template("bible/main.html")
