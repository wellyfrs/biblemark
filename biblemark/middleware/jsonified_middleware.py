import functools
import traceback

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

bp = Blueprint("jsonified", __name__)


def jsonified(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            data = view(**kwargs)
            return jsonify(data)
        except HTTPException as error:
            traceback.print_exc()
            return jsonify({
                "code": error.code,
                "name": error.name,
                "description": error.description,
            }), error.code
        except Exception:  # too broad exception clause is desired
            traceback.print_exc()
            return jsonify({
                "code": 500,
                "name": "Internal Server Error",
                "description": "Oops! An error occurred."
            }), 500

    return wrapped_view
