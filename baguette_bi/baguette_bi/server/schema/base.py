from pydantic import BaseModel


class Base(BaseModel):
    class Meta:
        orm_mode = True
