from typing import Union
import pydantic as _pydantic


# Schéma de la class Utilisateur (Users)


class _UserBase(_pydantic.BaseModel):
    email: str
    pseudo: str


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


class _ContactBase(_pydantic.BaseModel):
    id_user: int
    types: str
    contenu: str


class ContactCreate(_ContactBase):
    hashed_password: str

    class Config:
        orm_mode = True


class Contact(_ContactBase):
    id: int

    class Config:
        orm_mode = True
