# -*- coding: utf-8 -*-
import inspect
import json
from typing import Type, TypeVar, Union

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record

T = TypeVar('T')
RKind = Union[T, Type[T]]  # type:ignore


class JsonDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(
        record: RKind[Record], mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:  # type:ignore
        json_data: bytes = str(json.loads(data)).encode('utf-8')
        _rv = None

        if inspect.isclass(record):
            _record = record()
            _rv = mapper.map_deserialize(_record, json_data)  # type: ignore
        else:
            _rv = mapper.map_deserialize(record, json_data)  # type: ignore

        return _rv  # type:ignore


JsonDeserializer.deserialize.__doc__ = BaseDeserializer.deserialize.__doc__
