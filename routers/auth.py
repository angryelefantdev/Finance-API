from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from database import Session
from dependencies import get_db,get_current_user
from schemas.users import UserCreate,FetchUser
from models.users import Users
from dependencies import SECRET_KEY,ALGORITHM


password_hasher = PasswordHash((Argon2Hasher(),))

router = APIRouter()

@router.post("/register")
def register(user:UserCreate,db:Session = Depends(get_db)):
    usera = db.query(Users).filter(Users.username == user.username).first()
    if usera:
        raise HTTPException(status_code=400,detail="Already exists")
    hashed_pw = password_hasher.hash(user.password)
    new_user = Users(username=user.username,hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"Created account for {new_user.username}"}

@router.post("/auth/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(
        Users.username == form_data.username
    ).first()

    if not user or not password_hasher.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = jwt.encode(
        {"sub": user.username},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def getme(myself=Depends(get_current_user)):
    return {"username": myself.username, "id": myself.id}

