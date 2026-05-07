from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Avaliacao(SQLModel, table=True):
    __tablename__ = 'avaliacoes'

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    produto_id: int = Field(foreign_key='produtos.id')
    nota: int
    comentario: str | None = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
