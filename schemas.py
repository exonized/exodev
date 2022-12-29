from typing import Union
import pydantic as _pydantic


# Schéma de la class Utilisateur (Users)


class _UserBase(_pydantic.BaseModel):
    email: str
    pseudo: str
    adresse: str
    complement: str
    codepostal: int
    region: str
    numerorue: int


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    roles: str
    avatar: str

    class Config:
        orm_mode = True


