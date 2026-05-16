from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Estoque(SQLModel, table=True):
    __tablename__ = 'estoque'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key='produtos.id', unique=True)
    quantidade: int
    atualizado_em: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={'onupdate': datetime.now(timezone.utc)},
    )
