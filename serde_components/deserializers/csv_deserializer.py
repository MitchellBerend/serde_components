import io
import csv
from typing import Iterable, Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

T = TypeVar('T')


class CsvDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(records: Iterable[T], mapper: Type[BaseMapper], data: bytes) -> Iterable[T]:
        """
        This method takes in a iterable over the records and maps the data from
        a given csv.

        It takes an iterable since a csv will contain rows which should
        correspond with a single record.
        """
        file_object = io.StringIO(data.decode('utf-8'))
        dict_reader = csv.DictReader(file_object)

        for record, row in zip(records, dict_reader):
            mapper.map_deserialize(record, str(row).encode('utf-8'))

        return records
