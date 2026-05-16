from typing import Optional
from sqlmodel import Field, SQLModel


class Endereco(SQLModel, table=True):
    __tablename__ = 'enderecos'  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    rua: str = Field(max_length=150)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=100)
    cep: str = Field(max_length=20)
