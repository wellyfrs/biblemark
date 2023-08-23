from werkzeug.exceptions import HTTPException


class UsernameUnavailableError(HTTPException):
    code = 400


class InvalidCredentialsError(HTTPException):
    code = 401
