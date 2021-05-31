from typing import Optional


class User:
    def __init__(
        self,
        username: str,
        *,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        is_active: bool = True,
        is_admin: bool = False,
    ):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.is_active = is_active
        self.is_admin = is_admin

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        name = " ".join(
            s
            for s in [self.first_name, self.middle_name, self.last_name]
            if s is not None
        )
        if name == "":
            return self.username
        return name
