# -*- coding: utf-8 -*-
import json
from typing import Type

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record


class JsonDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(
        record: Record, mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:
        json_data: bytes = str(json.loads(data)).encode('utf-8')
        mapper.map_deserialize(record, json_data)  # type: ignore

        return record


JsonDeserializer.deserialize.__doc__ = BaseDeserializer.deserialize.__doc__
