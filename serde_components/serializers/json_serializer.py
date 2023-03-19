# -*- coding: utf-8 -*-
import json
from typing import Any, Type, TypeVar

from .base import BaseSerializer
from ..mappers import BaseMapper


class JsonSerializer(BaseSerializer):
    @staticmethod
    def serialize(record: Any, mapper: Type[BaseMapper]) -> bytes:
        data: bytes = mapper.map_serialize(record)
        json_data: bytes = json.dumps(data.decode()).encode('utf-8')

        return json_data
