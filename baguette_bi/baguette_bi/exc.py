class BaguetteException(Exception):
    pass


class Unauthorized(BaguetteException):
    pass


class Forbidden(BaguetteException):
    pass


class NotFound(BaguetteException):
    pass


class Conflict(BaguetteException):
    pass
