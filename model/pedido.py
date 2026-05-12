from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Pedido(SQLModel, table=True):
    __tablename__ = 'pedidos' # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    total: float
    status: str = Field(max_length=50)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
