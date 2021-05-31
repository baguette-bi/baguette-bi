from baguette_bi.schema.base import Base


class BaseUser(Base):
    id: str
    email: str
    first_name: str
    last_name: str
    middle_name: str

    is_active: bool
    is_admin: bool


class UserList(BaseUser):
    pass


class UserCreate(BaseUser):
    password: str


class UserRead(BaseUser):
    pass
