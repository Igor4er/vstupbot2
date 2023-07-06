from pydantic import BaseModel


class SupaBase(BaseModel):
    uuid: str | None
    created_at: str | None
    
    def zero(self):
        self.uuid = None
        self.created_at = None


class Categories(SupaBase):
    name: str


class Coeficients(SupaBase):
    math: float
    ukrainian: float
    foreign: float
    history: float
    physics: float
    chemestry: float
    biology: float


class Specialities(SupaBase):
    code: str
    name: str
    category: Categories


class Users(SupaBase):
    first_name: str
    last_name: str
    username: str
    language: str
