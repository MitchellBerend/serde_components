# -*- coding: utf-8 -*-
import ast
import json
from typing import Generic, Type

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record


class JsonDeserializer(BaseDeserializer, Generic[Record]):
    @staticmethod
    def deserialize(record: Record, mapper: Type[BaseMapper[Record]]) -> bytes:
        _data: bytes = mapper.map_deserialize(record)  # type: ignore
        data = ast.literal_eval(_data.decode('utf-8'))
        json_data: bytes = json.dumps(data).encode('utf-8')

        return json_data


JsonDeserializer.deserialize.__doc__ = BaseDeserializer.deserialize.__doc__
