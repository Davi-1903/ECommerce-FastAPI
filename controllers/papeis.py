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
def get_roles(session: SessionDep):
    return session.exec(select(Papel)).all()


@router.get('/papeis/{id}', response_model=Papel)
def get_role(id: int, session: SessionDep):
    role = session.get(Papel, id)
    if not role:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    return role


@router.post('/papeis', response_model=Papel)
def add_role(role: PapelInput, session: SessionDep):
    new_role = Papel(nome=role.nome)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role


@router.put('/papeis/{id}', response_model=Papel)
def edit_role(id: int, role: PapelInput, session: SessionDep):
    existing = session.get(Papel, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    existing.nome = role.nome
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/papeis/{id}', response_model=Papel)
def delete_role(id: int, session: SessionDep):
    existing = session.get(Papel, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/user-papeis', response_model=Sequence[UsuarioPapel])
def get_user_roles(session: SessionDep):
    return session.exec(select(UsuarioPapel)).all()


@router.post('/user-papeis', response_model=UsuarioPapel)
def add_user_role(relation: UsuarioPapelInput, session: SessionDep):
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
def delete_user_role(usuario_id: int, papel_id: int, session: SessionDep):
    relation = session.get(UsuarioPapel, (usuario_id, papel_id))
    if not relation:
        raise HTTPException(status_code=404, detail='Relação usuário-papel não encontrada')
    session.delete(relation)
    session.commit()
    return relation
