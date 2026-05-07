from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Estoque(SQLModel, table=True):
    __tablename__ = 'estoque'

    id: int | None = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key='produtos.id', unique=True)
    quantidade: int
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
