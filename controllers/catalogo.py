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
def get_products(session: SessionDep):
    return session.exec(select(Produto)).all()


@router.get('/produtos/{id}', response_model=Produto)
def get_product(id: int, session: SessionDep):
    product = session.get(Produto, id)
    if not product:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return product


@router.post('/produtos', response_model=Produto)
def add_product(product: ProdutoInput, session: SessionDep):
    new_product = Produto(nome=product.nome, descricao=product.descricao, preco=product.preco)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@router.put('/produtos/{id}', response_model=Produto)
def edit_product(id: int, product: ProdutoInput, session: SessionDep):
    existing = session.get(Produto, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    existing.nome = product.nome
    existing.descricao = product.descricao
    existing.preco = product.preco
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/produtos/{id}', response_model=Produto)
def delete_product(id: int, session: SessionDep):
    existing = session.get(Produto, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/categorias', response_model=Sequence[Categoria])
def get_categories(session: SessionDep):
    return session.exec(select(Categoria)).all()


@router.get('/categorias/{id}', response_model=Categoria)
def get_category(id: int, session: SessionDep):
    category = session.get(Categoria, id)
    if not category:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return category


@router.post('/categorias', response_model=Categoria)
def add_category(category: CategoriaInput, session: SessionDep):
    new_category = Categoria(nome=category.nome)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


@router.put('/categorias/{id}', response_model=Categoria)
def edit_category(id: int, category: CategoriaInput, session: SessionDep):
    existing = session.get(Categoria, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    existing.nome = category.nome
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/categorias/{id}', response_model=Categoria)
def delete_category(id: int, session: SessionDep):
    existing = session.get(Categoria, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/produto-categorias', response_model=Sequence[ProdutoCategoria])
def get_product_categories(session: SessionDep):
    return session.exec(select(ProdutoCategoria)).all()


@router.post('/produto-categorias', response_model=ProdutoCategoria)
def add_product_category(relation: ProdutoCategoriaInput, session: SessionDep):
    new_relation = ProdutoCategoria(produto_id=relation.produto_id, categoria_id=relation.categoria_id)
    session.add(new_relation)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_relation


@router.delete('/produto-categorias/{produto_id}/{categoria_id}', response_model=ProdutoCategoria)
def delete_product_category(produto_id: int, categoria_id: int, session: SessionDep):
    relation = session.get(ProdutoCategoria, (produto_id, categoria_id))
    if not relation:
        raise HTTPException(status_code=404, detail='Relação produto-categoria não encontrada')
    session.delete(relation)
    session.commit()
    return relation


@router.get('/estoque', response_model=Sequence[Estoque])
def get_stock(session: SessionDep):
    return session.exec(select(Estoque)).all()


@router.get('/estoque/{stock_id}', response_model=Estoque)
def get_stock_item(stock_id: int, session: SessionDep):
    stock = session.get(Estoque, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    return stock


@router.post('/estoque', response_model=Estoque)
def add_stock(stock: EstoqueInput, session: SessionDep):
    new_stock = Estoque(produto_id=stock.produto_id, quantidade=stock.quantidade)
    session.add(new_stock)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    session.refresh(new_stock)
    return new_stock


@router.put('/estoque/{id}', response_model=Estoque)
def edit_stock(id: int, stock: EstoqueInput, session: SessionDep):
    existing = session.get(Estoque, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    existing.produto_id = stock.produto_id
    existing.quantidade = stock.quantidade
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/estoque/{id}', response_model=Estoque)
def delete_stock(id: int, session: SessionDep):
    existing = session.get(Estoque, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Registro de estoque não encontrado')
    session.delete(existing)
    session.commit()
    return existing
