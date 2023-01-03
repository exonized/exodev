from typing import List

import fastapi
from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as _security

from fastapi import Depends, FastAPI, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session


import crud
import models
import schemas
from database import SessionLocal, engine

import sqlalchemy.orm as _orm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

conf = ConnectionConfig(
    MAIL_USERNAME="exodev@outlook.fr",
    MAIL_PASSWORD="Bs)Aa,LQ&3R-ee3",
    MAIL_FROM="exodev@outlook.fr",
    MAIL_PORT=587,
    MAIL_SERVER="smtp-mail.outlook.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


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

# Contact


@app.post("/api/contact", tags=["Contact"])
async def contact_create(contact: schemas.Contact = fastapi.Depends(crud.create_contact)):
    return contact


@app.get("/api/me/contact", tags=["Contact"])
async def get_me_contact(contact: schemas.Contact = fastapi.Depends(crud.get_me_contact)):
    return contact


@app.get("/api/me/contact/{id}", tags=["Contact"])
async def get_me_contact_id(contact: schemas.Contact = fastapi.Depends(crud.get_me_contact_id)):
    return contact


@app.delete("/api/me/contact/delete/{id}", tags=["Contact"])
async def delete_contact(id: int, contact: schemas.Contact = fastapi.Depends(crud.delete_contact)):
    return {"supprimer": contact}


# Blog

@app.post("/api/blog", tags=["Blog"])
async def blog_create(blog: schemas.Blog = fastapi.Depends(crud.create_blog)):
    return blog


@app.get("/api/get/blog", tags=["Blog"])
async def get_blog(blog: schemas.Blog = fastapi.Depends(crud.get_blog)):
    return blog


@app.delete("/api/blog/delete/{id}", tags=["Blog"])
async def delete_blog(id: int, blog: schemas.Blog = fastapi.Depends(crud.delete_blog)):
    return {"supprimer": blog}


# Projets

@app.post("/api/projet", tags=["Projet"])
async def projet_create(projet: schemas.Projet = fastapi.Depends(crud.create_projet)):
    return projet


@app.get("/api/get/projet", tags=["Projet"])
async def get_projet(projet: schemas.Projet = fastapi.Depends(crud.get_projet)):
    return projet


@app.delete("/api/projet/delete/{id}", tags=["Projet"])
async def delete_projet(id: int, projet: schemas.Projet = fastapi.Depends(crud.delete_projet)):
    return {"supprimer": projet}

# API  (Base)


@app.get("/", tags=["api"])
def read_services():
    return "Bienvenue sur ExoDEV"


@app.post("/email", tags=["api"])
async def envois_email(email: schemas.EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="ExoDEV - Vous avez reçu un nouveau message !",
        recipients=email.dict().get("email"),
        body=email.contenu,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Votre message à bien était envoyer"})
