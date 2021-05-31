import shlex
import subprocess
from contextlib import contextmanager

import psycopg2
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import wait_for


def stop(name, fail=False):
    """Stops a running postgres container"""
    cmd = shlex.split(f"docker stop {name}")
    try:
        subprocess.check_call(cmd)
    except subprocess.SubprocessError:
        if fail:
            raise


@contextmanager
def postgres_in_docker(port=5432):
    name = "baguette-bi-test-pg"
    cmd = shlex.split(
        f"docker run -d --rm -p {port}:5432 --name {name} "
        "-e POSTGRES_USER=test "
        "-e POSTGRES_PASSWORD=test "
        "postgres"
    )
    subprocess.check_call(cmd)
    params = dict(
        host="localhost", port=port, dbname="test", user="test", password="test"
    )

    def postgres_up():
        psycopg2.connect(**params)
        return True

    wait_for(postgres_up, 30, 1)

    yield "postgresql+psycopg2://test:test@localhost:{port}/test".format(port=port)
    stop(name)


@pytest.fixture(scope="session")
def db():
    from baguette_bi.server.models.base import Base

    with postgres_in_docker() as uri:
        engine = create_engine(uri)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session


@pytest.fixture(scope="session")
def engine(db):
    yield db.bind
