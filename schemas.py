from typing import Union
import pydantic as _pydantic
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

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


# Schéma de la class Contact (Contact)

class _ContactBase(_pydantic.BaseModel):
    types: str
    contenu: str


class ContactCreate(_ContactBase):

    class Config:
        orm_mode = True


class Contact(_ContactBase):
    id: int
    email: str
    id_user: int
    etat = str

    class Config:
        orm_mode = True


# Schéma de la class Projet (Projet)

class _ProjetBase(_pydantic.BaseModel):
    titre: str
    types: str
    description: str
    contenu: str
    images: str


class ProjetCreate(_ProjetBase):

    class Config:
        orm_mode = True


class Projet(_ProjetBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


# Schéma de la class Blog (Blog)


class _BlogBase(_pydantic.BaseModel):
    titre: str
    types: str
    description: str
    contenu: str
    images: str


class BlogCreate(_BlogBase):

    class Config:
        orm_mode = True


class Blog(_BlogBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class EmailSchema(_pydantic.BaseModel):
    email: List[EmailStr]
    contenu: str
