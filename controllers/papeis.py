from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from model.papel import Papel
from model.usuario_papel import UsuarioPapel

router = APIRouter(prefix='', tags=['papeis'])
SessionDep = Annotated[Session, Depends(get_session)]


class PapelInput(SQLModel):
    nome: str


class UsuarioPapelInput(SQLModel):
    usuario_id: int
    papel_id: int


# --------------------------------------- Endpoints ---------------------------------------

@router.get('/papeis', response_model=Sequence[Papel])
def get_papeis(session: SessionDep):
    return session.exec(select(Papel)).all()


@router.get('/papeis/{id}', response_model=Papel)
def get_papel(session: SessionDep, id: int):
    papel = session.get(Papel, id)
    if not papel:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    return papel


@router.post('/papeis', response_model=Papel)
def add_papel(session: SessionDep, papel: PapelInput):
    new_papel = Papel(nome=papel.nome)
    session.add(new_papel)
    session.commit()
    session.refresh(new_papel)
    return new_papel


@router.put('/papeis/{id}', response_model=Papel)
def edit_papel(session: SessionDep, id: int, papel: PapelInput):
    existing = session.get(Papel, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    existing.nome = papel.nome
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/papeis/{id}', response_model=Papel)
def delete_papel(session: SessionDep, id: int):
    existing = session.get(Papel, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/user-papeis', response_model=Sequence[UsuarioPapel])
def get_user_papeis(session: SessionDep):
    return session.exec(select(UsuarioPapel)).all()


@router.post('/user-papeis', response_model=UsuarioPapel)
def add_user_papel(session: SessionDep, relation: UsuarioPapelInput):
    new_relation = UsuarioPapel(
        usuario_id=relation.usuario_id,
        papel_id=relation.papel_id,
    )
    session.add(new_relation)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_relation


@router.delete('/user-papeis/{usuario_id}/{papel_id}', response_model=UsuarioPapel)
def delete_user_papel(session: SessionDep, usuario_id: int, papel_id: int):
    relation = session.get(UsuarioPapel, (usuario_id, papel_id))
    if not relation:
        raise HTTPException(status_code=404, detail='Relação usuário-papel não encontrada')
    session.delete(relation)
    session.commit()
    return relation
