from werkzeug.exceptions import HTTPException


class MarkNotFound(HTTPException):
    code = 404


class InvalidMarkedVerse(HTTPException):
    code = 400
