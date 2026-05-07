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
def get_orders(session: SessionDep):
    return session.exec(select(Pedido)).all()


@router.get('/pedidos/{id}', response_model=Pedido)
def get_order(id: int, session: SessionDep):
    order = session.get(Pedido, id)
    if not order:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    return order


@router.post('/pedidos', response_model=Pedido)
def add_order(order: PedidoInput, session: SessionDep):
    new_order = Pedido(usuario_id=order.usuario_id, total=order.total, status=order.status)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order


@router.put('/pedidos/{id}', response_model=Pedido)
def edit_order(id: int, order: PedidoInput, session: SessionDep):
    existing = session.get(Pedido, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    existing.usuario_id = order.usuario_id
    existing.total = order.total
    existing.status = order.status
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/pedidos/{id}', response_model=Pedido)
def delete_order(id: int, session: SessionDep):
    existing = session.get(Pedido, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/pedidos-items', response_model=Sequence[ItemPedido])
def get_order_items(session: SessionDep):
    return session.exec(select(ItemPedido)).all()


@router.get('/pedidos-items/{id}', response_model=ItemPedido)
def get_order_item(id: int, session: SessionDep):
    item = session.get(ItemPedido, id)
    if not item:
        raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
    return item


@router.post('/pedidos-items', response_model=ItemPedido)
def add_order_item(item: ItemPedidoInput, session: SessionDep):
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


@router.put('/pedidos-items/{id}', response_model=ItemPedido)
def edit_order_item(id: int, item: ItemPedidoInput, session: SessionDep):
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


@router.delete('/pedidos-items/{id}', response_model=ItemPedido)
def delete_order_item(id: int, session: SessionDep):
    existing = session.get(ItemPedido, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Item de pedido não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/payments', response_model=Sequence[Pagamento])
def get_payments(session: SessionDep):
    return session.exec(select(Pagamento)).all()


@router.get('/payments/{id}', response_model=Pagamento)
def get_payment(id: int, session: SessionDep):
    payment = session.get(Pagamento, id)
    if not payment:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return payment


@router.post('/payments', response_model=Pagamento)
def add_payment(payment: PagamentoInput, session: SessionDep):
    new_payment = Pagamento(
        pedido_id=payment.pedido_id,
        valor=payment.valor,
        metodo=payment.metodo,
        status=payment.status,
        pago_em=payment.pago_em,
    )
    session.add(new_payment)
    session.commit()
    session.refresh(new_payment)
    return new_payment


@router.put('/payments/{id}', response_model=Pagamento)
def edit_payment(id: int, payment: PagamentoInput, session: SessionDep):
    existing = session.get(Pagamento, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    existing.pedido_id = payment.pedido_id
    existing.valor = payment.valor
    existing.metodo = payment.metodo
    existing.status = payment.status
    existing.pago_em = payment.pago_em
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/payments/{id}', response_model=Pagamento)
def delete_payment(id: int, session: SessionDep):
    existing = session.get(Pagamento, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    session.delete(existing)
    session.commit()
    return existing
