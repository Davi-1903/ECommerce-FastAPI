from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.categoria import Categoria

router = APIRouter(prefix='/categorias', tags=['categorias'])
SessionDep = Annotated[Session, Depends(get_session)]


class CategoriaInput(SQLModel):
    nome: str


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Categoria])
def get_categorias(session: SessionDep, cursor: int, limit: int):
    statement = select(Categoria).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Categoria)
def get_categoria(session: SessionDep, id: int):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return categoria


@router.post('/', response_model=Categoria)
def add_categoria(session: SessionDep, categoria: CategoriaInput):
    try:
        new_categoria = Categoria(nome=categoria.nome)
        session.add(new_categoria)
        session.commit()
        session.refresh(new_categoria)
        return new_categoria

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Categoria)
def edit_categoria(session: SessionDep, id: int, categoria: CategoriaInput):
    try:
        existing = session.get(Categoria, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        existing.nome = categoria.nome
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Categoria)
def delete_categoria(session: SessionDep, id: int):
    try:
        existing = session.get(Categoria, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
