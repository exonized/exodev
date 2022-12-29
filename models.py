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
    adresse = Column(String)
    complement = Column(String)
    codepostal = Column(Integer)
    region = Column(String)
    numerorue = Column(Integer)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


