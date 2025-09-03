from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/coding-test")

engine = create_engine(url=DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
