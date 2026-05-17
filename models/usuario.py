from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from models.usuario_papel import UsuarioPapel


if TYPE_CHECKING:
    from models.papel import Papel
    from models.avaliacao import Avaliacao
    from models.endereco import Endereco
    from models.pedido import Pedido


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuarios'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(max_length=150, unique=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    papeis: List['Papel'] = Relationship(back_populates='usuarios', link_model=UsuarioPapel)
    avaliacoes: List['Avaliacao'] = Relationship(back_populates='usuario')
    endereco: Optional['Endereco'] = Relationship(back_populates='usuario')
    pedidos: List['Pedido'] = Relationship(back_populates='usuario')
