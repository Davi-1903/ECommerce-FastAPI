from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.produto import Produto
    from models.pedido import Pedido


class ItemPedido(SQLModel, table=True):
    __tablename__ = 'itens_pedido'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    produto_id: int = Field(foreign_key='produtos.id')
    quantidade: int
    preco: float

    produto: 'Produto' = Relationship(back_populates='item_pedido')
    pedido: 'Pedido' = Relationship(back_populates='item_pedido')
