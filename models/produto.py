from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Produto(SQLModel, table=True):
    __tablename__ = 'produtos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    descricao: str | None = None
    preco: float
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
