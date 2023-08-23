from flask import request, redirect, flash, render_template, url_for, Blueprint

from biblemark.service.auth_service import unauthenticate, authenticate, InvalidCredentialsError

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            authenticate(username=username, password=password)
        except InvalidCredentialsError:
            error = "Incorrect credentials."
        else:
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout", methods=["GET"])
def logout():
    unauthenticate()
    return redirect(url_for("index"))
