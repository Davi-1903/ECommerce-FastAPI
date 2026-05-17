from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from argon2 import PasswordHasher
from database import get_session
from models.usuario import Usuario

router = APIRouter(prefix='', tags=['usuários'])
SessionDep = Annotated[Session, Depends(get_session)]
ph = PasswordHasher()


class User(SQLModel):
    nome: str
    email: str
    senha: str


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/users', response_model=Sequence[Usuario])
def get_users(session: SessionDep):
    return session.exec(select(Usuario)).all()


@router.get('/users/{id}', response_model=Usuario)
def get_user(session: SessionDep, id: int):
    user = session.get(Usuario, id)
    if user is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return user


@router.post('/users', response_model=Usuario | None)
def add_user(session: SessionDep, user: User):
    try:
        new_user = Usuario(
            nome=user.nome,
            email=user.email,
            senha_hash=ph.hash(user.senha),
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/users', response_model=Usuario)
def edit_user(session: SessionDep, id: int, new_user: User):
    try:
        user = session.get(Usuario, id)
        if user is None:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        user.nome = new_user.nome
        user.email = new_user.email
        user.senha_hash = new_user.senha
        session.commit()
        return user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/users', response_model=Usuario | None)
def delete_user(session: SessionDep, id: int):
    try:
        user = session.get(Usuario, id)
        session.delete(user)
        session.commit()
        return user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
