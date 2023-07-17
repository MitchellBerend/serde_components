# -*- coding: utf-8 -*-
import ast
import json
from typing import Generic, Type

from .base import BaseSerializer
from ..mappers import BaseMapper
from ..record import Record


class JsonSerializer(BaseSerializer, Generic[Record]):
    @staticmethod
    def serialize(record: Record, mapper: Type[BaseMapper[Record]]) -> bytes:
        _data: bytes = mapper.map_serialize(record)  # type: ignore
        data = ast.literal_eval(_data.decode('utf-8'))
        json_data: bytes = json.dumps(data).encode('utf-8')

        return json_data


JsonSerializer.serialize.__doc__ = BaseSerializer.serialize.__doc__
