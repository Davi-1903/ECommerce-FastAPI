from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Pagamento(SQLModel, table=True):
    __tablename__ = 'pagamentos'

    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    valor: float
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: datetime | None = None
