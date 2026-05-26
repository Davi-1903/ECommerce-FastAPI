from time import sleep
from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from os import getenv


def get_env(key: str, default: str | None = None) -> str:
    '''
    Função responsável por pegar variáveis de ambiente e verificar sua existência

    :param key: Nome da variável de ambiente
    :type key: str
    :param default: Valor caso a variável não exista (opcional)
    :type default: str | None
    :return: Valor da variável ou valor default
    :return type: str
    '''

    load_dotenv()

    value = getenv(key)
    if value is not None and value != '':
        return value
    if default is not None:
        return default
    raise RuntimeError(f'A variável de ambiente "{key}" não foi definida.')


def get_engine(**kargs) -> Engine:
    '''
    Função responsável por tentar estabelecer uma conexão com banco de dados. Ele fará 10 tentativas de estabelecer uma conexão, caso falhe, ele esperará 3 segundos. Com o término das 10 tentativas será lançado um erro `RuntimeError`

    :param **kargs: Parâmetros de `create_engine` do [SQLModel](https://sqlmodel.tiangolo.com/);
    :return: engine do banco de dados
    :return type: Engine
    '''

    for _ in range(10):
        try:
            engine = create_engine(**kargs)
            engine.connect()
            return engine
        except OperationalError:
            sleep(3)
    raise RuntimeError('Não foi possível estabelecer uma conexão com o banco de dados')


def create_url() -> str:
    '''
    Função responsável por pegar variáveis de ambiente e montar URL para o banco de dados

    :return: URL para o banco de dados
    :return type: str
    '''
    
    host = get_env('DB_HOST')
    port = get_env('DB_PORT')
    name = get_env('DB_NAME')
    user = get_env('DB_USER')
    password = get_env('DB_PASSWORD', '')

    if password == '':
        return f'mysql+pymysql://{user}@{host}:{port}/{name}'
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'
