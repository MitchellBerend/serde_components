# -*- coding: utf-8 -*-
import abc
from typing import Generic, IO, Iterable, Type, Union

from ..mappers import BaseMapper
from ..record import Record

RKind = Union[Iterable[Record], Type[Record]]


class BaseDeserializer(abc.ABC, Generic[Record]):
    """
    This base class defines the interface that all deserializers must
    implement. All methods that require implementation are marked with the
    @abc.abstractmethod decorator.

    Because this base does not know about the derived deserializers desired
    format, everything string like is passed as a utf-8 encoded bytestring.
    """

    @staticmethod
    @abc.abstractmethod
    def deserialize(
        record: RKind[Record], mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.

        Args:
            record: Some concrete record instance that inherits from
                BaseRecord.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.

        Returns:
            The passed record with data mapped from the data.
        """
        raise NotImplementedError

    @classmethod
    def deserialize_from_file(
        cls,
        record: RKind[Record],
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Record:
        """
        A convenience method that reads data from a file object and maps it to
        the record with the passed in mapper.

        Args:
            record: Some concrete record instance that inherits from
                BaseRecord.
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
        data = file_object.read()
        return cls.deserialize(record, mapper, data)
