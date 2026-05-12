from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuarios' # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(max_length=150, unique=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
