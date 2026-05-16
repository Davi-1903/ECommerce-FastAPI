from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.endereco import Endereco
from models.avaliacao import Avaliacao

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
def get_endereco(session: SessionDep):
    return session.exec(select(Endereco)).all()


@router.get('/endereco/{endereco_id}', response_model=Endereco)
def get_endereco(session: SessionDep, endereco_id: int):
    address = session.get(Endereco, endereco_id)
    if not address:
        raise HTTPException(status_code=404, detail='Endereço não encontrado')
    return address


@router.post('/endereco', response_model=Endereco)
def add_endereco(session: SessionDep, endereco: EnderecoInput):
    try:
        new_endereco = Endereco(
            usuario_id=endereco.usuario_id,
            rua=endereco.rua,
            cidade=endereco.cidade,
            estado=endereco.estado,
            cep=endereco.cep,
        )
        session.add(new_endereco)
        session.commit()
        session.refresh(new_endereco)
        return new_endereco

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/endereco/{id}', response_model=Endereco)
def edit_endereco(session: SessionDep, id: int, endereco: EnderecoInput):
    try:
        existing = session.get(Endereco, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Endereço não encontrado')
        existing.usuario_id = endereco.usuario_id
        existing.rua = endereco.rua
        existing.cidade = endereco.cidade
        existing.estado = endereco.estado
        existing.cep = endereco.cep
        session.commit()
        session.refresh(existing)
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/endereco/{id}', response_model=Endereco)
def delete_endereco(session: SessionDep, id: int):
    try:
        existing = session.get(Endereco, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Endereço não encontrado')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/reviews', response_model=Sequence[Avaliacao])
def get_reviews(session: SessionDep):
    return session.exec(select(Avaliacao)).all()


@router.get('/reviews/{id}', response_model=Avaliacao)
def get_review(session: SessionDep, id: int):
    review = session.get(Avaliacao, id)
    if not review:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')
    return review


@router.post('/reviews', response_model=Avaliacao)
def add_review(session: SessionDep, review: AvaliacaoInput):
    try:
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

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/reviews/{id}', response_model=Avaliacao)
def edit_review(session: SessionDep, id: int, review: AvaliacaoInput):
    try:
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

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/reviews/{id}', response_model=Avaliacao)
def delete_review(session: SessionDep, id: int):
    try:
        existing = session.get(Avaliacao, id)
        if not existing:
            raise HTTPException(status_code=404, detail='Avaliação não encontrada')
        session.delete(existing)
        session.commit()
        return existing

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
