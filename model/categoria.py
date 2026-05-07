from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    __tablename__ = 'categorias'

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
