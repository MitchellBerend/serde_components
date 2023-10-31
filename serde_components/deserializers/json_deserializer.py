# -*- coding: utf-8 -*-
import ast
import json
from typing import Generic, Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

T = TypeVar('T')


class JsonDeserializer(BaseDeserializer, Generic[T]):
    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper[T]]) -> bytes:
        _data: bytes = mapper.map_deserialize(record)
        data = ast.literal_eval(_data.decode('utf-8'))
        json_data: bytes = json.dumps(data).encode('utf-8')

        return json_data


JsonDeserializer.deserialize.__doc__ = BaseDeserializer.deserialize.__doc__
