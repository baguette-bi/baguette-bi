from baguette_bi import schema
from baguette_bi.server import models


class UserList(schema.UserList):
    pass


class UserCreate(schema.UserCreate):
    def create(self):
        user = models.User(**self.dict(exclude={"password"}))
        user.set_password(self.password)
        return user


class UserRead(schema.UserRead):
    pass
