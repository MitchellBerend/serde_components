# -*- coding: utf-8 -*-
import ast
import io
import csv
from typing import Generic, IO, Type, TypeVar
from typing import Iterable as Iter

from .base import BaseDeserializer
from ..mappers import BaseMapper


T = TypeVar('T')


class CsvDeserializer(BaseDeserializer, Generic[T]):
    @staticmethod
    def deserialize(records: Iter[T], mapper: Type[BaseMapper[T]]) -> bytes:
        """
        This method takes in a iterable over the records and maps the data from
        a to a csv format. It takes an iterable since a csv will contain rows
        which should correspond with a single record.

        This class takes a different type than the BaseDeserializer, it does
        not make sense for a csv deserializer to only map a single record. For
        this reason the type checking is ignored.

        Args:
            records: Some iterable of concrete record instances.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.

        Returns:
            A bytestring of the data encoded by the specific Deserializer.
        """
        mapped_data = []
        for record in records:
            b_data: bytes = mapper.map_deserialize(record)  # type:ignore
            data = b_data.decode('utf-8')
            mapped_data.append(ast.literal_eval(data))

        assert len(mapped_data) >= 1

        keys = list(mapped_data[0].keys())
        file_object = io.StringIO('')

        writer = csv.DictWriter(file_object, fieldnames=keys, dialect='unix')
        writer.writeheader()
        for row in mapped_data:
            writer.writerow(row)

        return file_object.getvalue().encode('utf-8')

    @classmethod
    def deserialize_to_file(
        cls, record: Iter[T], mapper: Type[BaseMapper], file_object: IO[bytes]
    ) -> None:
        """
        A convenience method that maps the record with the passed in mapper and
        writes it to a file object.
        This method only gets overwriten to change the accepted types.

        Args:
            record: Some concrete record instance.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            file_object: Some file-like object that can be read from. This
                includes io.BytesIO and file objects opened in byte mode.

        Raises:
            ValueError: An error has occured while doing I/O operations.
        """
        r = record
        m = mapper
        f = file_object
        return super().deserialize_to_file(r, m, f)
