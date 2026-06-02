from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from database import get_session
from models.pedido import Pedido
from models.item_pedido import ItemPedido

router = APIRouter(prefix='/pedidos', tags=['pedidos'])
SessionDep = Annotated[Session, Depends(get_session)]


class PedidoInput(BaseModel):
    usuario_id: int
    total: float
    status: str


class ItemPedidoInput(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int
    preco: float


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Pedido])
def get_pedidos(session: SessionDep, cursor: int, limit: int):
    statement = select(Pedido).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Pedido)
def get_pedido(session: SessionDep, id: int):
    pedido = session.get(Pedido, id)
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    return pedido


@router.post('/', response_model=Pedido)
def add_pedido(session: SessionDep, pedido: PedidoInput):
    try:
        new_pedido = Pedido(
            usuario_id=pedido.usuario_id, total=pedido.total, status=pedido.status
        )
        session.add(new_pedido)
        session.commit()
        session.refresh(new_pedido)
        return new_pedido

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Pedido)
def edit_pedido(session: SessionDep, id: int, pedido: PedidoInput):
    try:
        existing = session.get(Pedido, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        existing.usuario_id = pedido.usuario_id
        existing.total = pedido.total
        existing.status = pedido.status
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Pedido)
def delete_pedido(session: SessionDep, id: int):
    try:
        existing = session.get(Pedido, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/items', response_model=Sequence[ItemPedido])
def get_pedido_items(session: SessionDep, cursor: int, limit: int):
    statement = select(ItemPedido).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/items/{id}', response_model=ItemPedido)
def get_pedido_item(session: SessionDep, id: int):
    item = session.get(ItemPedido, id)
    if not item:
        raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
    return item


@router.post('/items', response_model=ItemPedido)
def add_pedido_item(session: SessionDep, item: ItemPedidoInput):
    try:
        new_item = ItemPedido(
            pedido_id=item.pedido_id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco=item.preco,
        )
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
        return new_item

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/items/{id}', response_model=ItemPedido)
def edit_pedido_item(session: SessionDep, id: int, item: ItemPedidoInput):
    try:
        existing = session.get(ItemPedido, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
        existing.pedido_id = item.pedido_id
        existing.produto_id = item.produto_id
        existing.quantidade = item.quantidade
        existing.preco = item.preco
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/items/{id}', response_model=ItemPedido)
def delete_pedido_item(session: SessionDep, id: int):
    try:
        existing = session.get(ItemPedido, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
