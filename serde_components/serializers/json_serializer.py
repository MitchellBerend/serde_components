# -*- coding: utf-8 -*-
import inspect
import json
from typing import Type, TypeVar, Union

from .base import BaseSerializer
from ..mappers import BaseMapper

T = TypeVar('T')
RKind = Union[T, Type[T]]


class JsonSerializer(BaseSerializer[T]):
    @staticmethod
    def serialize(record: RKind[T], mapper: Type[BaseMapper[T]], data: bytes) -> T:
        """This docstring gets overwritten with the original one."""
        json_data: bytes = str(json.loads(data)).encode('utf-8')
        _rv = None

        if inspect.isclass(record):
            _record = record()
            _rv = mapper.map_serialize(_record, json_data)
        else:
            _rv = mapper.map_serialize(record, json_data)

        return _rv


JsonSerializer.serialize.__doc__ = BaseSerializer.serialize.__doc__
