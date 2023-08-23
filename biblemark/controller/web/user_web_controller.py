from flask import Blueprint, request, redirect, url_for, flash, render_template, g

from biblemark.middleware.authenticated_middleware import authenticated
from biblemark.model.user import User
from biblemark.repository.mark_repository import count_highlights_by_user, count_notes_by_user
from biblemark.service.user_service import UsernameUnavailableError, register_user

bp = Blueprint("user", __name__)


def validate_registration_form(form_data):
    username = form_data.get("username")
    name = form_data.get("name")
    password = form_data.get("password")
    confirmation = form_data.get("confirmation")

    if not username or not name or not password or not confirmation:
        return "Username, name, password and password confirmation are required."

    if password != confirmation:
        return "Passwords do not match."

    return None


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        error = validate_registration_form(form_data)

        if error is None:
            try:
                register_user(
                    User(username=form_data["username"], name=form_data["name"], password=form_data["password"]))
            except UsernameUnavailableError:
                error = f"User {form_data['username']} is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("user/register.html")


@bp.route("/profile", methods=["GET"])
@authenticated
def profile():
    highlights = count_highlights_by_user(g.principal)
    notes = count_notes_by_user(g.principal)

    return render_template("user/profile.html",
                           user=g.principal,
                           highlights=highlights,
                           notes=notes,
                           )
