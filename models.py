from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import passlib.hash as _hash
from database import Base
from sqlalchemy.sql import func
from datetime import datetime


class User(Base):
    __tablename__ = "Utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    pseudo = Column(String, unique=True, index=True)
    roles = Column(String,  default=('Membre'))
    avatar = Column(String, default=('Avatar/base.png'))
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Contact(Base):
    __tablename__ = "Contact"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer)
    types = Column(String)
    contenu = Column(String)
    etat = Column(String,  default=('Non traité'))


class Projet(Base):
    __tablename__ = "Projet"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    types = Column(String)
    description = Column(String)
    contenu = Column(String)
    images = Column(String)
    date = Column(TIMESTAMP(timezone=False),
                  nullable=False, default=datetime.now())


class Blog(Base):
    __tablename__ = "Blog"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    types = Column(String)
    description = Column(String)
    contenu = Column(String)
    images = Column(String)
    date = Column(TIMESTAMP(timezone=False),
                  nullable=False, default=datetime.now())
