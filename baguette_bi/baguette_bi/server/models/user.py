from sqlalchemy import Column, Integer, String

from baguette_bi.server import crypto
from baguette_bi.server.models.base import Base


class User(Base):
    username = Column(String, primary_key=True)
    password_hash = Column(String, nullable=False)

    session_counter = Column(Integer, nullable=False, default=0)

    def set_password(self, password: str):
        if self.session_counter is None:
            self.session_counter = 1
        self.password_hash = crypto.pwd_context.hash(password)

    def check_password(self, password: str):
        return crypto.pwd_context.verify(password, self.password_hash)
