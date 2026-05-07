from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from model.endereco import Endereco
from model.avaliacao import Avaliacao

router = APIRouter(prefix='', tags=['endereços'])
SessionDep = Annotated[Session, Depends(get_session)]


class EnderecoInput(SQLModel):
    usuario_id: int
    rua: str
    cidade: str
    estado: str
    cep: str


class AvaliacaoInput(SQLModel):
    usuario_id: int
    produto_id: int
    nota: int
    comentario: str | None = None


# --------------------------------------- Endpoints ---------------------------------------

@router.get('/endereco', response_model=Sequence[Endereco])
def get_addresses(session: SessionDep):
    return session.exec(select(Endereco)).all()


@router.get('/endereco/{address_id}', response_model=Endereco)
def get_address(address_id: int, session: SessionDep):
    address = session.get(Endereco, address_id)
    if not address:
        raise HTTPException(status_code=404, detail='Endereço não encontrado')
    return address


@router.post('/endereco', response_model=Endereco)
def add_address(address: EnderecoInput, session: SessionDep):
    new_address = Endereco(
        usuario_id=address.usuario_id,
        rua=address.rua,
        cidade=address.cidade,
        estado=address.estado,
        cep=address.cep,
    )
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    return new_address


@router.put('/endereco/{id}', response_model=Endereco)
def edit_address(id: int, address: EnderecoInput, session: SessionDep):
    existing = session.get(Endereco, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Endereço não encontrado')
    existing.usuario_id = address.usuario_id
    existing.rua = address.rua
    existing.cidade = address.cidade
    existing.estado = address.estado
    existing.cep = address.cep
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/endereco/{id}', response_model=Endereco)
def delete_address(id: int, session: SessionDep):
    existing = session.get(Endereco, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Endereço não encontrado')
    session.delete(existing)
    session.commit()
    return existing


@router.get('/reviews', response_model=Sequence[Avaliacao])
def get_reviews(session: SessionDep):
    return session.exec(select(Avaliacao)).all()


@router.get('/reviews/{id}', response_model=Avaliacao)
def get_review(id: int, session: SessionDep):
    review = session.get(Avaliacao, id)
    if not review:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')
    return review


@router.post('/reviews', response_model=Avaliacao)
def add_review(review: AvaliacaoInput, session: SessionDep):
    new_review = Avaliacao(
        usuario_id=review.usuario_id,
        produto_id=review.produto_id,
        nota=review.nota,
        comentario=review.comentario,
    )
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


@router.put('/reviews/{id}', response_model=Avaliacao)
def edit_review(id: int, review: AvaliacaoInput, session: SessionDep):
    existing = session.get(Avaliacao, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')
    existing.usuario_id = review.usuario_id
    existing.produto_id = review.produto_id
    existing.nota = review.nota
    existing.comentario = review.comentario
    session.commit()
    session.refresh(existing)
    return existing


@router.delete('/reviews/{id}', response_model=Avaliacao)
def delete_review(id: int, session: SessionDep):
    existing = session.get(Avaliacao, id)
    if not existing:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')
    session.delete(existing)
    session.commit()
    return existing
