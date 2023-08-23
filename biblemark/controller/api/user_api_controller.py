from flask import Blueprint, g

from biblemark.middleware.authenticated_middleware import authenticated
from biblemark.middleware.jsonified_middleware import jsonified

bp = Blueprint("api/user", __name__, url_prefix="/api")


@bp.route("/me")
@authenticated
@jsonified
def me():
    """Endpoint to retrieve authenticated user"""
    return {
        "user": {
            "id": g.principal.entity_id,
            "username": g.principal.username,
            "name": g.principal.name,
            "created": g.principal.created,
        }
    }
