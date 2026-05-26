from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.pagamento import Pagamento

router = APIRouter(prefix='/pagamentos', tags=['pagamentos'])
SessionDep = Annotated[Session, Depends(get_session)]


class PagamentoInput(SQLModel):
    pedido_id: int
    valor: float
    metodo: str
    status: str


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Pagamento])
def get_pagamentos(session: SessionDep, cursor: int, limit: int):
    statement = select(Pagamento).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Pagamento)
def get_pagamento(session: SessionDep, id: int):
    pagamento = session.get(Pagamento, id)
    if not pagamento:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return pagamento


@router.post('/', response_model=Pagamento)
def add_pagamento(session: SessionDep, pagamento: PagamentoInput):
    try:
        new_pagamento = Pagamento(
            pedido_id=pagamento.pedido_id,
            valor=pagamento.valor,
            metodo=pagamento.metodo,
            status=pagamento.status,
        )
        session.add(new_pagamento)
        session.commit()
        session.refresh(new_pagamento)
        return new_pagamento

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Pagamento)
def edit_pagamento(session: SessionDep, id: int, pagamento: PagamentoInput):
    try:
        existing = session.get(Pagamento, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Pagamento não encontrado')
        existing.pedido_id = pagamento.pedido_id
        existing.valor = pagamento.valor
        existing.metodo = pagamento.metodo
        existing.status = pagamento.status
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Pagamento)
def delete_pagamento(session: SessionDep, id: int):
    try:
        existing = session.get(Pagamento, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Pagamento não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
