# -*- coding: utf-8 -*-
import ast
from typing import Any, Dict, Type

from .base import BaseSerializer
from ..mappers import BaseMapper
from .xml import XmlWriter as xml


class XmlSerializer(BaseSerializer):
    @staticmethod
    def serialize(record: Any, mapper: Type[BaseMapper]) -> bytes:
        data: str = mapper.map_serialize(record).decode('utf-8')
        data_dict: Dict[str, Any] = ast.literal_eval(data)
        xml_data: bytes = xml.dumps(data_dict)

        return xml_data
