from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from database import get_session
from models.usuario import Usuario
from utils import create_access_token, decode_access_token


router = APIRouter(prefix='/auth', tags=['Autenticação'])
SessionDep = Annotated[Session, Depends(get_session)]
oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/login')
ph = PasswordHash.recommended()


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRegister(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


def get_current_user(session: SessionDep, token: str = Depends(oauth2)) -> Usuario:
    try:
        email = decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail='Token inválido')

    user = session.scalar(select(Usuario).where(Usuario.email == email))
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return user


# --------------------------------------- Endpoints ---------------------------------------


@router.post('/register', response_model=Token)
def register(session: SessionDep, user_input: UserRegister):
    try:
        user = Usuario(
            nome=user_input.nome,
            email=user_input.email,
            senha_hash=ph.hash(user_input.senha)
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            'access_token': create_access_token({'sub': user.email}),
            'token_type': 'Bearer'
        }
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail='Credenciais inválidas',
            headers={'WWW-Authenticate': 'Bearer'}
        )


@router.post('/login', response_model=Token)
def login(session: SessionDep, user_input: UserLogin):
    usuario = session.scalar(select(Usuario).where(Usuario.email == user_input.email))
    if not usuario or not ph.verify(user_input.senha, usuario.senha_hash):
        raise HTTPException(status_code=400, detail='Erro')
    
    return {
        'access_token': create_access_token({'sub': usuario.email}),
        'token_type': 'Bearer'
    }


@router.post('/me', response_model=Usuario)
def get_user(user: Usuario = Depends(get_current_user)):
    return user
