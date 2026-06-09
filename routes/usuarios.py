from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from database import get_session
from models.usuario import Usuario
from utils import create_hash

router = APIRouter(prefix='/usuarios', tags=['usuários'])
SessionDep = Annotated[Session, Depends(get_session)]


class UserInput(BaseModel):
    nome: str
    email: EmailStr
    senha: str


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Usuario])
def get_(session: SessionDep, cursor: int, limit: int):
    statement = select(Usuario).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Usuario)
def get_user(session: SessionDep, id: int):
    user = session.get(Usuario, id)
    if user is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return user


@router.post('/', response_model=Usuario | None)
def add_user(session: SessionDep, user: UserInput):
    try:
        new_user = Usuario(
            nome=user.nome,
            email=user.email,
            senha_hash=create_hash(user.senha),
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/', response_model=Usuario)
def edit_user(session: SessionDep, id: int, new_user: UserInput):
    try:
        user = session.get(Usuario, id)
        if user is None:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        user.nome = new_user.nome
        user.email = new_user.email
        user.senha_hash = create_hash(new_user.senha)
        session.commit()
        return user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/', response_model=Usuario | None)
def delete_user(session: SessionDep, id: int):
    try:
        user = session.get(Usuario, id)
        session.delete(user)
        session.commit()
        return user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
