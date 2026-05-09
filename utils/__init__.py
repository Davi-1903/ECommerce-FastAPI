from dotenv import load_dotenv
from os import getenv


def get_env(key: str) -> str:
    load_dotenv()

    value = getenv(key)
    if value is None or value == '':
        raise RuntimeError(f'A variável de ambiente "{key}" não foi definida.')
    return value
