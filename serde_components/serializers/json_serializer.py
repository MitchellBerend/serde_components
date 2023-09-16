# -*- coding: utf-8 -*-
import inspect
import json
from typing import Type, TypeVar, Union

from .base import BaseSerializer
from ..mappers import BaseMapper
from ..record import Record

T = TypeVar('T')
RKind = Union[T, Type[T]]  # type:ignore


class JsonSerializer(BaseSerializer[Record]):
    @staticmethod
    def serialize(  # type:ignore
        record: RKind[Record], mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:  # type:ignore
        """This docstring gets overwritten with the original one."""
        json_data: bytes = str(json.loads(data)).encode('utf-8')
        _rv = None

        if inspect.isclass(record):
            _record = record()
            _rv = mapper.map_serialize(_record, json_data)  # type: ignore
        else:
            _rv = mapper.map_serialize(record, json_data)  # type: ignore

        return _rv  # type:ignore


JsonSerializer.serialize.__doc__ = BaseSerializer.serialize.__doc__
