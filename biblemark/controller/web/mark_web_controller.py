from flask import g, render_template, Blueprint, request

from biblemark.converter.mark_converters import serialize_enriched_mark
from biblemark.converter.pagination_converter import build_paginated_response
from biblemark.middleware.authenticated_middleware import authenticated
from biblemark.repository.mark_repository import count_highlights_by_user, count_notes_by_user
from biblemark.service.mark_service import get_highlights_by_user, get_notes_by_user

bp = Blueprint("mark", __name__)


DEFAULT_PAGE_SIZE = 30


def validate_page_size(page_size):
    if page_size not in [1, 5, 10, 30, 50, 100]:
        raise ValueError("Invalid page size as pagination parameter")


@bp.route("/highlights", methods=["GET"])
@authenticated
def highlights():
    page_size = request.args.get("size", default=DEFAULT_PAGE_SIZE, type=int)
    validate_page_size(page_size)

    page_number = max(1, request.args.get("page", default=1, type=int)) - 1

    total_elements = count_highlights_by_user(g.principal)

    content = get_highlights_by_user(g.principal, page_number, page_size)
    serialized = list(map(lambda item: serialize_enriched_mark(item["mark"], item["passages"]), content))
    paginated = build_paginated_response(page_size, total_elements, page_number, serialized)

    return render_template(
        "marks/highlights.html",
        colors=list({item["color"] for item in paginated["content"] if "color" in item}),
        marks=paginated["content"],
        size=paginated["page"]["size"],
        elements=paginated["page"]["totalElements"],
        pages=paginated["page"]["totalPages"],
        page=paginated["page"]["number"]+1
    )


@bp.route("/notes", methods=["GET"])
@authenticated
def notes():
    page_size = request.args.get("size", default=DEFAULT_PAGE_SIZE, type=int)
    validate_page_size(page_size)

    page_number = max(1, request.args.get("page", default=1, type=int)) - 1

    total_elements = count_notes_by_user(g.principal)

    content = get_notes_by_user(g.principal, page_number, page_size)
    serialized = list(map(lambda item: serialize_enriched_mark(item["mark"], item["passages"]), content))
    paginated = build_paginated_response(page_size, total_elements, page_number, serialized)

    return render_template(
        "marks/notes.html",
        marks=paginated["content"],
        size=paginated["page"]["size"],
        elements=paginated["page"]["totalElements"],
        pages=paginated["page"]["totalPages"],
        page=(paginated["page"]["number"] + 1)
    )
