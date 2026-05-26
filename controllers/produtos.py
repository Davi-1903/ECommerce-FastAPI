from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.produto import Produto
from models.produto_categoria import ProdutoCategoria

router = APIRouter(prefix='/produtos', tags=['produtos'])
SessionDep = Annotated[Session, Depends(get_session)]


class ProdutoInput(SQLModel):
    nome: str
    descricao: str | None = None
    preco: float


class ProdutoCategoriaInput(SQLModel):
    produto_id: int
    categoria_id: int


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Produto])
def get_produtos(session: SessionDep, cursor: int, limit: int):
    statement = select(Produto).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Produto)
def get_produto(session: SessionDep, id: int):
    produto = session.get(Produto, id)
    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto


@router.post('/', response_model=Produto)
def add_produto(session: SessionDep, produto: ProdutoInput):
    try:
        new_produto = Produto(
            nome=produto.nome, descricao=produto.descricao, preco=produto.preco
        )
        session.add(new_produto)
        session.commit()
        session.refresh(new_produto)
        return new_produto

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=Produto)
def edit_produto(session: SessionDep, id: int, produto: ProdutoInput):
    try:
        existing = session.get(Produto, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Produto não encontrado')
        existing.nome = produto.nome
        existing.descricao = produto.descricao
        existing.preco = produto.preco
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=Produto)
def delete_produto(session: SessionDep, id: int):
    try:
        existing = session.get(Produto, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Produto não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/categorias', response_model=Sequence[ProdutoCategoria])
def get_produto_categorias(session: SessionDep, cursor: int, limit: int):
    statement = select(ProdutoCategoria).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.post('/categorias', response_model=ProdutoCategoria)
def add_produto_categoria(session: SessionDep, relation: ProdutoCategoriaInput):
    try:
        new_relation = ProdutoCategoria(
            produto_id=relation.produto_id, categoria_id=relation.categoria_id
        )
        session.add(new_relation)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return new_relation

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/categorias/{produto_id}/{categoria_id}', response_model=ProdutoCategoria)
def delete_produto_categoria(session: SessionDep, produto_id: int, categoria_id: int):
    try:
        relation = session.get(ProdutoCategoria, (produto_id, categoria_id))
        if not relation:
            raise HTTPException(
                status_code=404, detail='Relação produto-categoria não encontrada'
            )
        session.delete(relation)
        session.commit()
        return relation

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
