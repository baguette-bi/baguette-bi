from typing import Any, Optional

from fastapi import HTTPException

from baguette_bi.exc import BaguetteException


class ServerException(BaguetteException):
    def __init__(self, status_code: int, detail: Optional[Any] = None):
        self.status_code = status_code
        self.detail = detail


class WebException(ServerException):
    """Exception for web views"""


class APIException(HTTPException):
    """Exception for API endpoints"""
