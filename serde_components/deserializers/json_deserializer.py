# -*- coding: utf-8 -*-
import json
from typing import Type

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import BaseRecord as R


class JsonDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(record: R, mapper: Type[BaseMapper], data: bytes) -> R:
        json_data: bytes = str(json.loads(data)).encode('utf-8')
        mapper.map_deserialize(record, json_data)

        return record
