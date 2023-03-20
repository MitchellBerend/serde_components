# -*- coding: utf-8 -*-
import ast
import io
import csv
from typing import Iterable, Type, TypeVar

from .base import BaseSerializer
from ..mappers import BaseMapper

T = TypeVar('T')


class CsvSerializer(BaseSerializer):
    @staticmethod
    def serialize(records: Iterable[T], mapper: Type[BaseMapper]) -> bytes:
        """
        This method takes in a iterable over the records and maps the data from
        a to a csv format.

        It takes an iterable since a csv will contain rows which should
        correspond with a single record.
        """
        mapped_data = []
        for record in records:
            b_data: bytes = mapper.map_serialize(record)
            data = b_data.decode('utf-8')
            mapped_data.append(ast.literal_eval(data))

        assert len(mapped_data) > 1

        keys = list(mapped_data[0].keys())
        file_object = io.StringIO('')

        writer = csv.DictWriter(file_object, fieldnames=keys, dialect='unix')
        writer.writeheader()
        for row in mapped_data:
            writer.writerow(row)

        return file_object.getvalue().encode('utf-8')
