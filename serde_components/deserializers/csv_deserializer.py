# -*- coding: utf-8 -*-
import io
import csv
from typing import Generic, IO, Type, TypeVar
from typing import Iterable as Iter

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record


class CsvDeserializer(BaseDeserializer, Generic[Record]):
    @staticmethod
    def deserialize(  # type: ignore
        records: Iter[Record], mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Iter[Record]:
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

        return [
            mapper.map_deserialize(record, str(row).encode('utf-8'))  # type: ignore
            for record, row in zip(records, dict_reader)
        ]

    @classmethod
    def deserialize_from_file(  # type: ignore
        cls,
        record: Iter[Record],
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Iter[Record]:
        """
        This method only gets overwriten to change the accepted types.
        """
        r = record
        m = mapper
        f = file_object
        return super().deserialize_from_file(r, m, f)  # type: ignore
