# -*- coding: utf-8 -*-
import ast
import io
import csv
from typing import Generic, IO, Type
from typing import Iterable as Iter

from .base import BaseSerializer
from ..mappers import BaseMapper
from ..record import Record


class CsvSerializer(BaseSerializer, Generic[Record]):
    @staticmethod
    def serialize(records: Iter[Record], mapper: Type[BaseMapper[Record]]) -> bytes:  # type: ignore
        """
        This method takes in a iterable over the records and maps the data from
        a to a csv format. It takes an iterable since a csv will contain rows
        which should correspond with a single record.

        This class takes a different type than the BaseSerializer, it does not
        make sense for a csv serializer to only map a single record. For this
        reason the type checking is ignored.
        """
        mapped_data = []
        for record in records:
            b_data: bytes = mapper.map_serialize(record)  # type: ignore
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

    @classmethod
    def serialize_to_file(  # type: ignore
        cls, record: Iter[Record], mapper: Type[BaseMapper], file_object: IO[bytes]
    ) -> None:
        """
        This method only gets overwriten to change the accepted types.
        """
        r = record
        m = mapper
        f = file_object
        return super().serialize_to_file(r, m, f)  # type: ignore
