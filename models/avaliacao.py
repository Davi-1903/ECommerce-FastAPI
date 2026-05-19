from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.usuario import Usuario
    from models.produto import Produto


class Avaliacao(SQLModel, table=True):
    __tablename__ = 'avaliacoes'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    produto_id: int = Field(foreign_key='produtos.id')
    comentario: str | None = None
    nota: int
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    usuario: 'Usuario' = Relationship(back_populates='avaliacoes')
    produto: 'Produto' = Relationship(back_populates='avaliacoes')
