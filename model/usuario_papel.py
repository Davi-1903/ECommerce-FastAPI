from sqlmodel import Field, SQLModel


class UsuarioPapel(SQLModel, table=True):
    __tablename__ = 'usuario_papeis'

    usuario_id: int = Field(foreign_key='usuarios.id', primary_key=True)
    papel_id: int = Field(foreign_key='papeis.id', primary_key=True)
