# -*- coding: utf-8 -*-
import ast
import json
from typing import Any, Type, TypeVar

from .base import BaseSerializer
from ..mappers import BaseMapper


class JsonSerializer(BaseSerializer):
    @staticmethod
    def serialize(record: Any, mapper: Type[BaseMapper]) -> bytes:
        _data: bytes = mapper.map_serialize(record)
        data = ast.literal_eval(_data.decode('utf-8'))
        json_data: bytes = json.dumps(data).encode('utf-8')

        return json_data
