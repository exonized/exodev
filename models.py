from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import passlib.hash as _hash
from database import Base


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
