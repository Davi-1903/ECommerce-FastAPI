from typing import Optional
from sqlmodel import Field, SQLModel


class ItemPedido(SQLModel, table=True):
    __tablename__ = 'itens_pedido'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    produto_id: int = Field(foreign_key='produtos.id')
    quantidade: int
    preco: float
