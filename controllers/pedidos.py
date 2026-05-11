from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from model.pedido import Pedido
from model.item_pedido import ItemPedido
from model.pagamento import Pagamento

router = APIRouter(prefix='', tags=['pedidos'])
SessionDep = Annotated[Session, Depends(get_session)]


class PedidoInput(SQLModel):
    usuario_id: int
    total: float
    status: str


class ItemPedidoInput(SQLModel):
    pedido_id: int
    produto_id: int
    quantidade: int
    preco: float


class PagamentoInput(SQLModel):
    pedido_id: int
    valor: float
    metodo: str
    status: str
    pago_em: str | None = None


# --------------------------------------- Endpoints ---------------------------------------

@router.get('/pedidos', response_model=Sequence[Pedido])
def get_pedidos(session: SessionDep):
    return session.exec(select(Pedido)).all()


@router.get('/pedidos/{id}', response_model=Pedido)
def get_pedido(session: SessionDep, id: int):
    pedido = session.get(Pedido, id)
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    return pedido


@router.post('/pedidos', response_model=Pedido)
def add_pedido(session: SessionDep, pedido: PedidoInput):
    try:
        new_pedido = Pedido(usuario_id=pedido.usuario_id, total=pedido.total, status=pedido.status)
        session.add(new_pedido)
        session.commit()
        session.refresh(new_pedido)
        return new_pedido
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/pedidos/{id}', response_model=Pedido)
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


@router.delete('/pedidos/{id}', response_model=Pedido)
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


@router.get('/pedidos-items', response_model=Sequence[ItemPedido])
def get_pedido_items(session: SessionDep):
    return session.exec(select(ItemPedido)).all()


@router.get('/pedidos-items/{id}', response_model=ItemPedido)
def get_pedido_item(session: SessionDep, id: int):
    item = session.get(ItemPedido, id)
    if not item:
        raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
    return item


@router.post('/pedidos-items', response_model=ItemPedido)
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


@router.put('/pedidos-items/{id}', response_model=ItemPedido)
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


@router.delete('/pedidos-items/{id}', response_model=ItemPedido)
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


@router.get('/pagamentos', response_model=Sequence[Pagamento])
def get_pagamentos(session: SessionDep):
    return session.exec(select(Pagamento)).all()


@router.get('/pagamentos/{id}', response_model=Pagamento)
def get_pagamento(session: SessionDep, id: int):
    pagamento = session.get(Pagamento, id)
    if not pagamento:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return pagamento


@router.post('/pagamentos', response_model=Pagamento)
def add_pagamento(session: SessionDep, pagamento: PagamentoInput):
    try:
        new_pagamento = Pagamento(
            pedido_id=pagamento.pedido_id,
            valor=pagamento.valor,
            metodo=pagamento.metodo,
            status=pagamento.status,
            pago_em=pagamento.pago_em,
        )
        session.add(new_pagamento)
        session.commit()
        session.refresh(new_pagamento)
        return new_pagamento
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/pagamentos/{id}', response_model=Pagamento)
def edit_pagamento(session: SessionDep, id: int, pagamento: PagamentoInput):
    try:
        existing = session.get(Pagamento, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Pagamento não encontrado')
        existing.pedido_id = pagamento.pedido_id
        existing.valor = pagamento.valor
        existing.metodo = pagamento.metodo
        existing.status = pagamento.status
        existing.pago_em = pagamento.pago_em
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/pagamentos/{id}', response_model=Pagamento)
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
