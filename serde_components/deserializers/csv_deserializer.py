# -*- coding: utf-8 -*-
import io
import csv
from typing import Generic, IO, Type, TypeVar, Union
from typing import Iterable as Iter

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record

T = TypeVar('T')
RKind = Union[Iter[T], Type[T]]


class CsvDeserializer(BaseDeserializer, Generic[Record]):
    @staticmethod
    def deserialize(  # type: ignore
        records: RKind[Record], mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Iter[Record]:
        """
        This method takes in a iterable over the records and maps the data from
        a given csv. It takes an iterable since a csv will contain rows which
        should correspond with a single record.

        This class takes a different type than the BaseSerializer, it does not
        make sense for a csv serializer to only map a single record. For this
        reason the type checking is ignored.

        Args:
            records: Some iterable of concrete record instances that inherits
                from BaseRecord or a factory method that creates an instance of
                a record when called.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.

        Returns:
            The passed record with data mapped from the data.
        """
        file_object = io.StringIO(data.decode('utf-8'))
        dict_reader = csv.DictReader(file_object)

        if isinstance(records, Iter):
            return [
                mapper.map_deserialize(record, str(row).encode('utf-8'))  # type: ignore
                for record, row in zip(records, dict_reader)
            ]
        else:
            return [
                mapper.map_deserialize(
                    records(), str(row).encode('utf-8')  # type: ignore
                )
                for row in dict_reader
            ]

    @classmethod
    def deserialize_from_file(  # type: ignore
        cls,
        record: RKind[Record],
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Iter[Record]:
        """
        A convenience method that reads data from a file object and maps it to
        the record with the passed in mapper.

        This method only gets overwriten to change the accepted types, see
        BaseDeserializer for more details.

        Args:
            records: Some iterable of concrete record instances that inherits
                from BaseRecord or a factory method that creates an instance of
                a record when called.

            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.
            file_object: Some file-like object that can be read from. This
                includes io.BytesIO and file objects opened in byte mode.

        Returns:
            The passed record with data mapped from the data.

        Raises:
            ValueError: An error has occured while doing I/O operations.
        """
        r = record
        m = mapper
        f = file_object
        return super().deserialize_from_file(r, m, f)  # type: ignore
