import json
from typing import Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

T = TypeVar('T')


class JsonDeserializer(BaseDeserializer):

    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        json_data: bytes = json.loads(data).encode('utf-8')
        mapper.map_deserialize(record, json_data)

        return record
