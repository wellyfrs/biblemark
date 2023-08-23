from flask import render_template, Blueprint

bp = Blueprint("about", __name__)


@bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
