from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Pagamento(SQLModel, table=True):
    __tablename__ = 'pagamentos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    valor: float
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
