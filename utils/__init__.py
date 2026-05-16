from time import sleep
from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from os import getenv


def get_env(key: str) -> str:
    load_dotenv()

    value = getenv(key)
    if value is None or value == '':
        raise RuntimeError(f'A variável de ambiente "{key}" não foi definida.')
    return value


def get_engine(**kargs) -> Engine:
    for _ in range(10):
        try:
            engine = create_engine(**kargs)
            engine.connect()
            return engine
        except OperationalError:
            sleep(3)
    raise RuntimeError('Não foi possível estabelecer uma conexão com o banco de dados')
