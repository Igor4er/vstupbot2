from pydantic import BaseModel


class SupaBase(BaseModel):
    uuid: str | int | None = None
    created_at: str | None = None

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
    speciality: str


class Specialities(SupaBase):
    code: str
    name: str
    category: str


class Users(SupaBase):
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language: str


class Results(SupaBase):
    subject_name: str | None = None
    ua: int | None = None
    math: int | None = None
    third_subject: int | None = None
    user: int
