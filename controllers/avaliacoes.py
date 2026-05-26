from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.avaliacao import Avaliacao


router = APIRouter(prefix='/avaliacoes', tags=['avaliações'])
SessionDep = Annotated[Session, Depends(get_session)]


class AvaliacaoInput(SQLModel):
    usuario_id: int
    produto_id: int
    nota: int
    comentario: str | None = None


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Avaliacao])
def get_reviews(session: SessionDep, cursor: int, limit: int):
    statement = select(Avaliacao).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Avaliacao)
def get_review(session: SessionDep, id: int):
    review = session.get(Avaliacao, id)
    if not review:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')
    return review


@router.post('/', response_model=Avaliacao)
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


@router.put('/{id}', response_model=Avaliacao)
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


@router.delete('/{id}', response_model=Avaliacao)
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
