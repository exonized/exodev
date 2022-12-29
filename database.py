from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://fqxswkhkoqnzjl:0f9f266f4b5574ba8c99517a7c65eeb638f93a3f2f752f74fcec10d10e19ff3a@ec2-52-30-159-47.eu-west-1.compute.amazonaws.com:5432/d5a22lf72jchn"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
