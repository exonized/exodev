import sqlalchemy.orm as _orm

import passlib.hash as _hash
import jwt
import fastapi
import fastapi.security as _security
from sqlalchemy import or_

import models
import schemas
import database


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"


# Utilisateur

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_id(id: str, db: _orm.Session):
    return db.query(models.User).filter(models.User.id == id).first()


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer", roles=user.roles, email=user.email, id=user.id)


async def create_user(user: schemas.UserCreate, db: _orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password), pseudo=user.pseudo
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def get_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Mauvais email ou mot de passe"
        )

    return schemas.User.from_orm(user)


async def delete_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
        db.delete(user)
        db.commit()

    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Problème lors de la suppression"
        )

    return schemas.User.from_orm(user)


# Contact


async def create_contact(
    Contact: schemas.ContactCreate,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    user = db.query(models.User).get(payload["id"])

    contact_obj = models.Contact(
        id_user=user.id, types=Contact.types, contenu=Contact.contenu
    )
    db.add(contact_obj)
    db.commit()
    db.refresh(contact_obj)

    return (contact_obj)


async def get_me_contact(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    user = db.query(models.User).get(payload["id"])
    print(user.id)
    result = db.query(models.Contact).where(models.Contact.id_user == user.id)

    # contact = db.query(models.Contact).get(models.Contact.id_user == user.id)
    # contact = db.query(models.Contact).filter(
    #     user.id == models.Contact.id).all()

    return result


async def get_me_contact_id(
    id: int,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    contact = db.query(models.Contact).filter(
        models.Contact.id == id).all()

    return contact


async def delete_contact(
    id: int,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    contact = db.query(models.Contact).filter(models.Contact.id == id).delete()
    db.commit()

    return (contact)


# Blog

async def create_blog(
    Blog: schemas.BlogCreate,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    blog_obj = models.Blog(
        titre=Blog.titre, types=Blog.types, description=Blog.description, contenu=Blog.contenu, images=Blog.images
    )
    db.add(blog_obj)
    db.commit()
    db.refresh(blog_obj)

    return (blog_obj)


async def get_blog(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    blog = db.query(models.Blog).filter().all()
    return blog


async def delete_blog(
    id: int,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()

    return (blog)


# Projet


async def create_projet(
    Blog: schemas.ProjetCreate,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    projet_obj = models.Projet(
        titre=Blog.titre, types=Blog.types, description=Blog.description, contenu=Blog.contenu, images=Blog.images
    )
    db.add(projet_obj)
    db.commit()
    db.refresh(projet_obj)

    return (projet_obj)


async def get_projet(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    projet = db.query(models.Projet).filter().all()
    return projet


async def delete_projet(
    id: int,
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    projet = db.query(models.Projet).filter(models.Projet.id == id).delete()
    db.commit()

    return (projet)
