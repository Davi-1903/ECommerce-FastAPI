from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.estoque import Estoque

router = APIRouter(prefix='/estoque', tags=['estoque'])
SessionDep = Annotated[Session, Depends(get_session)]


class EstoqueInput(SQLModel):
    produto_id: int
    quantidade: int


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Estoque])
def get_estoque(session: SessionDep, cursor: int, limit: int):
    statement = select(Estoque).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{estoque_id}', response_model=Estoque)
def get_estoque_item(session: SessionDep, estoque_id: int):
    estoque = session.get(Estoque, estoque_id)
    if not estoque:
        raise HTTPException(
            status_code=404, detail='Registro de estoque não encontrado'
        )
    return estoque


@router.post('/', response_model=Estoque)
def add_estoque(session: SessionDep, estoque: EstoqueInput):
    try:
        new_estoque = Estoque(
            produto_id=estoque.produto_id, quantidade=estoque.quantidade
        )
        session.add(new_estoque)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        session.refresh(new_estoque)
        return new_estoque

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Estoque)
def edit_estoque(session: SessionDep, id: int, estoque: EstoqueInput):
    try:
        existing = session.get(Estoque, id)
        if not existing:
            raise HTTPException(
                status_code=404, detail='Registro de estoque não encontrado'
            )
        existing.produto_id = estoque.produto_id
        existing.quantidade = estoque.quantidade
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Estoque)
def delete_estoque(session: SessionDep, id: int):
    try:
        existing = session.get(Estoque, id)
        if not existing:
            raise HTTPException(
                status_code=404, detail='Registro de estoque não encontrado'
            )
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
