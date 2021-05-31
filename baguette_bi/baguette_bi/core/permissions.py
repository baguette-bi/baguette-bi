from enum import Enum
from typing import Optional


class Permissions(str, Enum):
    public = "public"
    authenticated = "authenticated"
    inherit = "inherit"
