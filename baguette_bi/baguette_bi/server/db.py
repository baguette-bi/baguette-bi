from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from baguette_bi.server import settings

engine = create_engine(settings.database_url)
Session = scoped_session(sessionmaker(bind=engine))


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
