import json
import os
from collections import UserDict
from collections.abc import MutableMapping
from pathlib import Path
from typing import List


class BaseSecret:
    def __init__(self):
        self._key = None

    def resolve(self):  # pragma: no cover
        raise NotImplementedError


class SecretDict(UserDict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for k, v in self.data.items():
            if isinstance(v, MutableMapping):
                self.data[k] = SecretDict(v)
            if isinstance(v, BaseSecret):
                v._key = k

    def __getitem__(self, key):
        item = self.data[key]
        if isinstance(item, BaseSecret):
            item = item.resolve()
            self.data[key] = item
        return item

    def dict(self):
        d = self
        if isinstance(self, BaseSecret):
            return self.resolve()
        if not isinstance(self, MutableMapping):
            return self
        if isinstance(self, SecretDict):
            d = self.data
        return {k: SecretDict.dict(v) for k, v in d.items()}


class EnvSecret(BaseSecret):
    def __init__(self, var: str):
        super().__init__()
        self.var = var

    def resolve(self):
        value = os.getenv(self.var)
        if value is None:
            raise KeyError(f"Env variable {self.var} not found")
        return value


class FileSecret(BaseSecret):
    def __init__(self, path: str, *paths: List[str]):
        super().__init__()
        paths = [path] + list(paths)
        self.paths = [Path(p) for p in paths]

    def read_path(self, path: Path):
        return path.read_text()

    def resolve(self):
        for path in self.paths:
            if not path.is_file():
                continue
            return self.read_path(path)
        raise FileNotFoundError(f"None of the files for {self._key} exist")


class JsonFileSecret(FileSecret):
    def read_path(self, path: Path):
        return json.loads(path.read_text())


class Secret:
    @staticmethod
    def from_env(var):
        return EnvSecret(var)

    @staticmethod
    def from_file(path, *paths):
        return FileSecret(path, *paths)

    @staticmethod
    def from_json_file(path, *paths):
        return JsonFileSecret(path, *paths)
