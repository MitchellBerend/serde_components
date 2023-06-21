# -*- coding: utf-8 -*-
from typing import Type, TypeVar
import sys

from .base import BaseDeserializer
from ..mappers import BaseMapper

PYTHON_VERSION_ERROR = 'Your python version does not support this component'


if sys.version_info.minor >= 11:
    import tomllib


T = TypeVar('T')


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        # tomllib.loads does not take in bytestrings like json.loads does
        _data: str = data.decode('utf-8')

        try:
            toml = tomllib.loads(_data)
        except NameError:
            raise ImportError(PYTHON_VERSION_ERROR)

        toml_data: bytes = str(toml).encode('utf-8')
        mapper.map_deserialize(record, toml_data)

        return record
