from werkzeug.exceptions import HTTPException


class VersionNotFound(HTTPException):
    code = 404


class BookNotFound(HTTPException):
    code = 404


class ChapterNotFound(HTTPException):
    code = 404


class InvalidBibleReference(HTTPException):
    code = 400


class InvalidBook(HTTPException):
    code = 400


class BookNotMappedInStructure(HTTPException):
    code = 500
