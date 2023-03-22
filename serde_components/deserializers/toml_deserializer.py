# -*- coding: utf-8 -*-
from typing import Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

try:
    import tomllib
except ModuleNotFoundError:
    from .toml import InternalTomlLibLoader as tomllib


T = TypeVar('T')


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        # tomllib.loads does not take in bytestrings like json.loads does
        _data: str = data.decode('utf-8')
        toml = tomllib.loads(_data)
        toml_data: bytes = str(toml).encode('utf-8')
        mapper.map_deserialize(record, toml_data)

        return record
