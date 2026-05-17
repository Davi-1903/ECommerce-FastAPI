from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.usuario import Usuario
    from models.pagamento import Pagamento
    from models.item_pedido import ItemPedido


class Pedido(SQLModel, table=True):
    __tablename__ = 'pedidos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    total: float
    status: str = Field(max_length=50)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    usuario: Optional['Usuario'] = Relationship(back_populates='pedidos')
    pagamento: Optional['Pagamento'] = Relationship(back_populates='pedido')
    item_pedido: Optional['ItemPedido'] = Relationship(back_populates='pedido')
