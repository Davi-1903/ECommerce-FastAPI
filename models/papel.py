from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from models.usuario_papel import UsuarioPapel


if TYPE_CHECKING:
    from models.usuario import Usuario


class Papel(SQLModel, table=True):
    __tablename__ = 'papeis'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50)

    usuarios: List['Usuario'] = Relationship(back_populates='papeis', link_model=UsuarioPapel)
