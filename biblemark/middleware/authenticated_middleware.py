import functools

from flask import g, redirect, session, url_for, Blueprint

from biblemark.repository.user_repository import fetch_user_by_id

bp = Blueprint("authenticated", __name__)


def authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.principal is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load():
    user_id = session.get("user_id")
    if user_id is None:
        g.principal = None
    else:
        g.principal = fetch_user_by_id(user_id)
