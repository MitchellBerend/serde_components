# -*- coding: utf-8 -*-
import ast
from typing import Any, Dict, Type

from .base import BaseSerializer
from ..mappers import BaseMapper
from .toml import InternalTomlLibWriter as tomllib


class TomlSerializer(BaseSerializer):
    @staticmethod
    def serialize(record: Any, mapper: Type[BaseMapper]) -> bytes:
        data: str = mapper.map_serialize(record).decode('utf-8')
        data_dict: Dict[str, Any] = ast.literal_eval(data)
        toml_data: bytes = tomllib.dumps(data_dict)

        return toml_data
