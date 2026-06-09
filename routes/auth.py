from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import BaseModel
from database import get_session
from models.usuario import Usuario
from utils import create_access_token, get_env, verify_hash
from jwt import decode


router = APIRouter(prefix='/auth', tags=['Autenticação'])
SessionDep = Annotated[Session, Depends(get_session)]
token_schema = OAuth2PasswordBearer(tokenUrl='token')


class Token(BaseModel):
    access_token: str
    token_type: str


def get_current_user(session: SessionDep, token: Annotated[str, Depends(token_schema)]) -> Usuario:
    try:
        payload = decode(token, get_env('SECRET_KEY'), algorithms=[get_env('ALGORITHMS')])
        email = payload.get('sub')
        if email is None:
            raise # Esse raise jogará direto para o except da função
        
        usuario = session.scalar(select(Usuario).where(Usuario.email == email))
        if usuario is None:
            raise # Esse raise jogará direto para o except da função
        return usuario

    except:
        raise HTTPException(
            status_code=401,
            detail='Permissão negada',
            headers={'WWW-Authenticate': 'Bearer'}
        )

# --------------------------------------- Endpoints ---------------------------------------
@router.post('/login', response_model=Token)
def login(session: SessionDep, form: OAuth2PasswordRequestForm = Depends()):
    usuario = session.scalar(select(Usuario).where(Usuario.email == form.username))
    if not usuario or not verify_hash(usuario.senha_hash, form.password):
        raise HTTPException(status_code=400, detail='Erro')
    
    return {
        'access_token': create_access_token({'sub': usuario.email}),
        'token_type': 'Bearer'
    }
