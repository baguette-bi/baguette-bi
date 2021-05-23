import os
from pathlib import Path

import pytest
from baguette_bi.core.secret import (
    EnvSecret,
    FileSecret,
    JsonFileSecret,
    Secret,
    SecretDict,
)


def test_env_secret_resolve():
    os.environ["TESTENVVAR"] = "testvalue"
    es = EnvSecret("TESTENVVAR")
    assert es.resolve() == "testvalue"


def test_env_secret_raises_key_error():
    es = EnvSecret("NOVARTEST")
    with pytest.raises(KeyError):
        es.resolve()


def test_file_secret_resolve(tmpdir):
    path = Path(tmpdir)
    secret_file = path / "secret"
    secret_file.write_text("testvalue")
    fs = FileSecret(secret_file)
    assert fs.resolve() == "testvalue"


def test_file_secret_multiple_files_resolve(tmpdir):
    path = Path(tmpdir)
    first = path / "first"  # doesn't exist
    second = path / "second"
    second.write_text("testvalue")
    fs = FileSecret(first, second)
    assert fs.resolve() == "testvalue"


def test_file_secret_raises_file_not_found():
    fs = FileSecret("/fake/path/one", "/fake/path/two")
    with pytest.raises(FileNotFoundError):
        fs.resolve()


def test_secret_dict_getitem():
    os.environ["ENVVAR"] = "testvalue"
    sd = SecretDict({"secret": EnvSecret("ENVVAR")})
    assert sd["secret"] == "testvalue"


def test_secret_dict_sets_key():
    sd = SecretDict({"secret": EnvSecret("ENVVAR")})
    assert sd.data["secret"]._key == "secret"


def test_secret_dict_nested_secret():
    os.environ["ENVVAR"] = "testvalue"
    sd = SecretDict({"not a secret": {"secret": EnvSecret("ENVVAR")}})
    assert isinstance(sd.data["not a secret"], SecretDict)
    assert sd["not a secret"]["secret"] == "testvalue"


def test_secret_dict_to_dict():
    os.environ["ENVVAR"] = "testvalue"
    sd = SecretDict({"what": 1, "not a secret": {"secret": EnvSecret("ENVVAR")}})
    d = sd.dict()
    assert d["not a secret"]["secret"] == "testvalue"


def test_secret_from_env():
    assert isinstance(Secret.from_env("TESTENV"), EnvSecret)


def test_secret_from_file():
    assert isinstance(Secret.from_file("something"), FileSecret)


def test_secret_from_json_file(tmpdir):
    assert isinstance(Secret.from_json_file("something"), JsonFileSecret)
    path = Path(tmpdir) / "test.json"
    path.write_text('{"test": "test"}')
    sd = SecretDict({"what": 1, "secret": Secret.from_json_file(path)})
    assert sd.dict() == {"what": 1, "secret": {"test": "test"}}
