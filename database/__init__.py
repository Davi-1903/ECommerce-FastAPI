from sqlmodel import SQLModel, Session, create_engine
from model import papel, user

DATABASE_URI = 'sqlite:///app.db'
args = {'check_same_thread': False}
engine = create_engine(DATABASE_URI, connect_args=args)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(bind=engine) as session:
        yield session
