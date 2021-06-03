from typing import Any, Optional

from fastapi import HTTPException, status


class BaguetteException(Exception):
    def __init__(self, status_code: int, detail: Optional[Any] = None):
        self.status_code = status_code
        self.detail = detail

    def raise_for_view(self):
        raise WebException(status_code=self.status_code, detail=self.detail)

    def raise_for_api(self):
        raise APIException(status_code=self.status_code, detail=self.detail)


class WebException(BaguetteException):
    """Exception for web views"""


class APIException(HTTPException):
    """Exception for API endpoints"""


class Unauthorized(BaguetteException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Unauthorized"


class Forbidden(BaguetteException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Forbidden"


class NotFound(BaguetteException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Not found"
