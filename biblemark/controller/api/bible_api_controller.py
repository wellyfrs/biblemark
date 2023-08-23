from flask import Blueprint

from biblemark.converter.bible_converters import build_chapter_content_response
from biblemark.middleware.jsonified_middleware import jsonified
from biblemark.service.bible_service import get_versions, get_books, get_chapters, get_chapter_content

bp = Blueprint("api/bible", __name__, url_prefix="/api")


@bp.route("/versions", methods=["GET"])
@jsonified
def retrieve_versions():
    """Endpoint for retrieving versions"""
    data = get_versions()
    return {"versions": data}


@bp.route("/versions/<version_id>/books", methods=["GET"])
@jsonified
def retrieve_books(version_id):
    """Endpoint for retrieving books of a specific version"""
    data = get_books(version_id)
    return {"books": data}


@bp.route("/versions/<version_id>/books/<book_id>/chapters", methods=["GET"])
@jsonified
def retrieve_chapters(version_id, book_id):
    """Endpoint for retrieving chapters of a specific book in a version"""
    data = get_chapters(version_id, book_id)
    return {"chapters": data}


@bp.route("/versions/<version_id>/books/<book_id>/chapters/<chapter_id>", methods=["GET"])
@jsonified
def retrieve_chapter_content(version_id, book_id, chapter_id):
    """Endpoint for retrieving a specific chapter content"""
    chapter_content = get_chapter_content(version_id, book_id, chapter_id)
    return build_chapter_content_response(version_id, chapter_content)
