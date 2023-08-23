from flask import Flask

from biblemark.config import cache
from biblemark.config import db
from biblemark.utils.helpers import date
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cache.init_app(app)

    from biblemark.controller.api import bible_api_controller
    app.register_blueprint(bible_api_controller.bp)

    from biblemark.controller.api import mark_api_controller
    app.register_blueprint(mark_api_controller.bp)

    from biblemark.controller.api import user_api_controller
    app.register_blueprint(user_api_controller.bp)

    from biblemark.controller.web import about_web_controller
    app.register_blueprint(about_web_controller.bp)

    from biblemark.controller.web import auth_web_controller
    app.register_blueprint(auth_web_controller.bp)

    from biblemark.controller.web import user_web_controller
    app.register_blueprint(user_web_controller.bp)

    from biblemark.controller.web import bible_web_controller
    app.register_blueprint(bible_web_controller.bp)

    from biblemark.controller.web import mark_web_controller
    app.register_blueprint(mark_web_controller.bp)

    from biblemark.middleware import authenticated_middleware
    app.register_blueprint(authenticated_middleware.bp)

    app.jinja_env.filters["date"] = date

    app.add_url_rule("/", endpoint="index")

    return app
