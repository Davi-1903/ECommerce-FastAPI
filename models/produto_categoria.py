from __future__ import annotations
from sqlmodel import Field, SQLModel


class ProdutoCategoria(SQLModel, table=True):
    __tablename__ = 'produto_categorias'  # type: ignore

    produto_id: int = Field(foreign_key='produtos.id', primary_key=True)
    categoria_id: int = Field(foreign_key='categorias.id', primary_key=True)
