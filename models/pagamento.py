from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.pedido import Pedido


class Pagamento(SQLModel, table=True):
    __tablename__ = 'pagamentos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    valor: float
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    pedido: Optional['Pedido'] = Relationship(back_populates='pagamento')
