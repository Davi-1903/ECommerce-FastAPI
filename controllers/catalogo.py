from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from model.produto import Produto
from model.categoria import Categoria
from model.produto_categoria import ProdutoCategoria
from model.estoque import Estoque

router = APIRouter(prefix='', tags=['catálogos'])
SessionDep = Annotated[Session, Depends(get_session)]


class ProdutoInput(SQLModel):
    nome: str
    descricao: str | None = None
    preco: float


class CategoriaInput(SQLModel):
    nome: str


class ProdutoCategoriaInput(SQLModel):
    produto_id: int
    categoria_id: int


class EstoqueInput(SQLModel):
    produto_id: int
    quantidade: int


# --------------------------------------- Endpoints ---------------------------------------

@router.get('/produtos', response_model=Sequence[Produto])
def get_produtos(session: SessionDep):
    return session.exec(select(Produto)).all()


@router.get('/produtos/{id}', response_model=Produto)
def get_produto(session: SessionDep, id: int):
    produto = session.get(Produto, id)
    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto


@router.post('/produtos', response_model=Produto)
def add_produto(session: SessionDep, produto: ProdutoInput):
    new_produto = Produto(nome=produto.nome, descricao=produto.descricao, preco=produto.preco)
    session.add(new_produto)
    session.commit()
    session.refresh(new_produto)
    return new_produto


@router.put('/produtos/{id}', response_model=Produto)
def edit_produto(session: SessionDep, id: int, produto: ProdutoInput):
    existing = session.get(Produto, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    existing.nome = produto.nome
    existing.descricao = produto.descricao
    existing.preco = produto.preco
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/produtos/{id}', response_model=Produto)
def delete_produto(session: SessionDep, id: int):
    existing = session.get(Produto, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/categorias', response_model=Sequence[Categoria])
def get_categorias(session: SessionDep):
    return session.exec(select(Categoria)).all()


@router.get('/categorias/{id}', response_model=Categoria)
def get_categoria(session: SessionDep, id: int):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return categoria


@router.post('/categorias', response_model=Categoria)
def add_categoria(session: SessionDep, categoria: CategoriaInput):
    new_categoria = Categoria(nome=categoria.nome)
    session.add(new_categoria)
    session.commit()
    session.refresh(new_categoria)
    return new_categoria


@router.put('/categorias/{id}', response_model=Categoria)
def edit_categoria(session: SessionDep, id: int, categoria: CategoriaInput):
    existing = session.get(Categoria, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    existing.nome = categoria.nome
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/categorias/{id}', response_model=Categoria)
def delete_categoria(session: SessionDep, id: int):
    existing = session.get(Categoria, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/produto-categorias', response_model=Sequence[ProdutoCategoria])
def get_produto_categorias(session: SessionDep):
    return session.exec(select(ProdutoCategoria)).all()


@router.post('/produto-categorias', response_model=ProdutoCategoria)
def add_produto_categoria(session: SessionDep, relation: ProdutoCategoriaInput):
    new_relation = ProdutoCategoria(produto_id=relation.produto_id, categoria_id=relation.categoria_id)
    session.add(new_relation)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_relation


@router.delete('/produto-categorias/{produto_id}/{categoria_id}', response_model=ProdutoCategoria)
def delete_produto_categoria(session: SessionDep, produto_id: int, categoria_id: int):
    relation = session.get(ProdutoCategoria, (produto_id, categoria_id))
    if not relation:
        raise HTTPException(status_code=404, detail='Relação produto-categoria não encontrada')
    session.delete(relation)
    session.commit()
    return relation


@router.get('/estoque', response_model=Sequence[Estoque])
def get_estoque(session: SessionDep):
    return session.exec(select(Estoque)).all()


@router.get('/estoque/{estoque_id}', response_model=Estoque)
def get_estoque_item(session: SessionDep, estoque_id: int):
    estoque = session.get(Estoque, estoque_id)
    if not estoque:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    return estoque


@router.post('/estoque', response_model=Estoque)
def add_estoque(session: SessionDep, estoque: EstoqueInput):
    new_estoque = Estoque(produto_id=estoque.produto_id, quantidade=estoque.quantidade)
    session.add(new_estoque)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    session.refresh(new_estoque)
    return new_estoque


@router.put('/estoque/{id}', response_model=Estoque)
def edit_estoque(session: SessionDep, id: int, estoque: EstoqueInput):
    existing = session.get(Estoque, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    existing.produto_id = estoque.produto_id
    existing.quantidade = estoque.quantidade
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/estoque/{id}', response_model=Estoque)
def delete_estoque(session: SessionDep, id: int):
    existing = session.get(Estoque, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    session.delete(existing)
    session.commit()
    return existing
