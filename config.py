import os

from flask.cli import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_BIBLE_APP_KEY = os.environ.get("API_BIBLE_APP_KEY")
    API_BIBLE_BASE_URL = os.environ.get("API_BIBLE_BASE_URL") or "https://api.scripture.api.bible"

    DATABASE_FILE = os.environ.get("DATABASE_FILE") or os.path.join(basedir, "biblemark.sqlite")
    DATABASE_SCHEMA_SCRIPT = os.environ.get("DATABASE_SCHEMA_SCRIPT") or os.path.join(basedir, "schema.sql")
    DATABASE_DATA_SCRIPT = os.environ.get("DATABASE_DATA_SCRIPT") or os.path.join(basedir, "data.sql")

    CACHE_DIR = os.environ.get("CACHE_DIR") or os.path.join(basedir, "cache")
    CACHE_THRESHOLD = os.environ.get("CACHE_THRESHOLD") or 1000
    CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT") or 3600  # 3600s = 1h

    DEFAULT_VERSION_ID = os.environ.get("DEFAULT_VERSION_ID") or "KJV"
    DEFAULT_BOOK_ID = os.environ.get("DEFAULT_BOOK_ID") or "JHN"
    DEFAULT_CHAPTER_ID = os.environ.get("DEFAULT_CHAPTER_ID") or "1"
