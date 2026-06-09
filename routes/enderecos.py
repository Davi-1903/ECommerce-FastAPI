from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from database import get_session
from models.endereco import Endereco

router = APIRouter(prefix='/enderecos', tags=['endereços'])
SessionDep = Annotated[Session, Depends(get_session)]


class EnderecoInput(BaseModel):
    usuario_id: int
    rua: str
    cidade: str
    estado: str
    cep: str


# --------------------------------------- Endpoints ---------------------------------------


@router.get('/', response_model=Sequence[Endereco])
def get_enderecos(session: SessionDep, cursor: int, limit: int):
    statement = select(Endereco).offset(cursor).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=Endereco)
def get_endereco(session: SessionDep, id: int):
    address = session.get(Endereco, id)
    if not address:
        raise HTTPException(status_code=404, detail='Endereço não encontrado')
    return address


@router.post('/', response_model=Endereco)
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


@router.put('/{id}', response_model=Endereco)
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


@router.delete('/{id}', response_model=Endereco)
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
