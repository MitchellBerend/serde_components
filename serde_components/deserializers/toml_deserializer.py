# -*- coding: utf-8 -*-
from typing import Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

try:
    import tomllib
except ModuleNotFoundError:

    class tomllib:
        @staticmethod
        def loads(data: bytes):
            raise NotImplementedError


T = TypeVar('T')


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        json_data: bytes = str(tomllib.loads(data)).encode('utf-8')
        mapper.map_deserialize(record, json_data)

        return record
