from flask import Blueprint, request, json, g, abort

from biblemark.converter.mark_converters import build_mark_creation_response, serialize_mark
from biblemark.middleware.authenticated_middleware import authenticated
from biblemark.middleware.jsonified_middleware import jsonified
from biblemark.repository.mark_repository import soft_delete_marked_verses_by_ids
from biblemark.service.mark_service import create_mark, remove_mark, update_note_content_by
from biblemark.service.mark_service import get_marks_by_user_and_chapter

bp = Blueprint("api/marks", __name__, url_prefix="/api/marks")


def validate_mark_payload(payload):
    mark = payload.get("mark", {})

    color = mark.get("color")
    note = mark.get("note")

    # highlight XOR note
    valid_combinations = [
        (color is not None and note is None),  # highlight
        (color is None and note is not None),  # note
    ]

    if not any(valid_combinations):
        raise ValueError("Invalid mark payload")


def validate_marked_verse_ids(input_marked_verse_ids):
    if not input_marked_verse_ids:
        abort(400, description="No marked verse IDs provided")


@bp.route("/versions/<version_id>/books/<book_id>/chapters/<chapter_id>", methods=["GET"])
@authenticated
@jsonified
def get_visible_marks_in_chapter(version_id, book_id, chapter_id):
    """Endpoint for retrieving visible marks in a chapter"""
    marks = get_marks_by_user_and_chapter(
        user=g.principal,
        version_id=version_id,
        book_id=book_id,
        chapter_id=chapter_id
    )
    return {
        "marks": list(map(serialize_mark, marks))
    }


@bp.route("/", methods=["POST"])
@authenticated
@jsonified
def create():
    """Endpoint for creating a mark"""
    payload = json.loads(request.data)
    validate_mark_payload(payload)

    data = create_mark(payload)
    return build_mark_creation_response(request=payload, mark=data)


@bp.route("/highlights", methods=["DELETE"])
@authenticated
@jsonified
def hide_verse_highlights():
    """Endpoint for hiding verse highlights"""
    input_marked_verse_ids = request.args.get("markedVerses")
    validate_marked_verse_ids(input_marked_verse_ids)

    marked_verse_ids = input_marked_verse_ids.split(",")
    soft_delete_marked_verses_by_ids(marked_verse_ids)


@bp.route("/<mark_id>", methods=["PATCH"])
@authenticated
@jsonified
def update_mark(mark_id):
    """Endpoint for updating a specific mark"""
    payload = json.loads(request.data)
    update_note_content_by(mark_id, payload)


@bp.route("/<mark_id>", methods=["DELETE"])
@authenticated
@jsonified
def delete_mark(mark_id):
    """Endpoint for deleting a specific mark"""
    return serialize_mark(remove_mark(mark_id))
