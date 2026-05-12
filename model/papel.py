from typing import Optional
from sqlmodel import Field, SQLModel


class Papel(SQLModel, table=True):
    __tablename__ = 'papeis' # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50)
