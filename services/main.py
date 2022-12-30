from typing import List

import fastapi
from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as _security

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud
import models
import schemas
from database import SessionLocal, engine

import sqlalchemy.orm as _orm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Users

@app.post("/api/users", tags=["Utilisateur"])
async def create_user(
    user: schemas.UserCreate, db: _orm.Session = fastapi.Depends(crud.get_db)
):
    db_user = await crud.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(
            status_code=400, detail="Votre email est déjà utilisé")

    user = await crud.create_user(user, db)

    return await crud.create_token(user)


@app.post("/api/token", tags=["Utilisateur"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(crud.get_db),
):
    user = await crud.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(
            status_code=401, detail="Utilisateur non enregistré")

    return await crud.create_token(user)


@app.get("/api/users/me", tags=["Utilisateur"], response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(crud.get_current_user)):
    return user


@app.delete("/api/user/me/delete", tags=["Utilisateur"])
async def delete_user(user: schemas.User = fastapi.Depends(crud.delete_current_user)):
    return user


# API  (Base)


# Contact

@app.post("/api/contact", tags=["Contact"])
async def create_user(
    contact: schemas.UserCreate
):
    return await crud.create_contact(contact)


@app.get("/", tags=["api"])
def read_services():
    return "API ANTHONY TEST"
