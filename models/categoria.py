from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

from models.produto_categoria import ProdutoCategoria


if TYPE_CHECKING:
    from models.produto import Produto


class Categoria(SQLModel, table=True):
    __tablename__ = 'categorias'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)

    produtos: List['Produto'] = Relationship(back_populates='categorias', link_model=ProdutoCategoria)
