# -*- coding: utf-8 -*-
import io
import csv
from typing import IO, Type
from typing import Iterable as Iter

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import BaseRecord as R


class CsvDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(  # type: ignore
        records: Iter[R], mapper: Type[BaseMapper], data: bytes
    ) -> Iter[R]:
        """
        This method takes in a iterable over the records and maps the data from
        a given csv. It takes an iterable since a csv will contain rows which
        should correspond with a single record.

        This class takes a different type than the BaseSerializer, it does not
        make sense for a csv serializer to only map a single record. For this
        reason the type checking is ignored.
        """
        file_object = io.StringIO(data.decode('utf-8'))
        dict_reader = csv.DictReader(file_object)

        for record, row in zip(records, dict_reader):
            mapper.map_deserialize(record, str(row).encode('utf-8'))

        return records

    @classmethod
    def deserialize_from_file(
        cls, record: Iter[R], mapper: Type[BaseMapper], file_object: IO[bytes]
    ) -> R:
        """
        This method only gets overwriten to change the accepted types.
        """
        r = record
        m = mapper
        f = file_object
        return super().deserialize_from_file(r, m, f)  # type: ignore
