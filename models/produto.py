from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

from models.produto_categoria import ProdutoCategoria


if TYPE_CHECKING:
    from models.categoria import Categoria
    from models.avaliacao import Avaliacao
    from models.estoque import Estoque


class Produto(SQLModel, table=True):
    __tablename__ = 'produtos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    descricao: str | None = None
    preco: float
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    categorias: List['Categoria'] = Relationship(back_populates='produtos', link_model=ProdutoCategoria)
    avaliacoes: List['Avaliacao'] = Relationship(back_populates='produto')
    estoque: Optional['Estoque'] = Relationship(back_populates='produto')
