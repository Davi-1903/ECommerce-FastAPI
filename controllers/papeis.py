from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.papel import Papel
from models.usuario_papel import UsuarioPapel

router = APIRouter(prefix='/papeis', tags=['papeis'])
SessionDep = Annotated[Session, Depends(get_session)]


class PapelInput(SQLModel):
    nome: str


class UsuarioPapelInput(SQLModel):
    usuario_id: int
    papel_id: int


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Papel])
def get_papeis(session: SessionDep, cursor: int, limit: int):
    statement = select(Papel).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Papel)
def get_papel(session: SessionDep, id: int):
    papel = session.get(Papel, id)
    if not papel:
        raise HTTPException(status_code=404, detail='Papel não encontrado')
    return papel


@router.post('/', response_model=Papel)
def add_papel(session: SessionDep, papel: PapelInput):
    try:
        new_papel = Papel(nome=papel.nome)
        session.add(new_papel)
        session.commit()
        session.refresh(new_papel)
        return new_papel

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Papel)
def edit_papel(session: SessionDep, id: int, papel: PapelInput):
    try:
        existing = session.get(Papel, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Papel não encontrado')
        existing.nome = papel.nome
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Papel)
def delete_papel(session: SessionDep, id: int):
    try:
        existing = session.get(Papel, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Papel não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/usuario', response_model=Sequence[UsuarioPapel])
def get_user_papeis(session: SessionDep, cursor: int, limit: int):
    statemente = select(UsuarioPapel).offset(cursor).limit(limit)
    return session.exec(statemente).all()


@router.post('/usuario', response_model=UsuarioPapel)
def add_user_papel(session: SessionDep, relation: UsuarioPapelInput):
    try:
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

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/usuario/{usuario_id}/{papel_id}', response_model=UsuarioPapel)
def delete_user_papel(session: SessionDep, usuario_id: int, papel_id: int):
    try:
        relation = session.get(UsuarioPapel, (usuario_id, papel_id))
        if not relation:
            raise HTTPException(
                status_code=404, detail='Relação usuário-papel não encontrada'
            )
        session.delete(relation)
        session.commit()
        return relation

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
