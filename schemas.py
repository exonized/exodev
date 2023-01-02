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
    types: str
    contenu: str


class ContactCreate(_ContactBase):

    class Config:
        orm_mode = True


class Contact(_ContactBase):
    id: int
    id_user: int
    etat = str

    class Config:
        orm_mode = True
