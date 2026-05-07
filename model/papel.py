from sqlmodel import Field, SQLModel


class Papel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50)
