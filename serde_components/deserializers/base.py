# -*- coding: utf-8 -*-
import abc
from typing import Generic, IO, Type

from ..mappers import BaseMapper
from ..record import Record


class BaseDeserializer(abc.ABC, Generic[Record]):
    """
    This base class defines the interface that all deserializers must implement.
    All methods that require implementation are marked with the
    @abc.abstractmethod decorator.

    Because this base does not know about the derived deserializers desired
    format, everything string like is passed as a utf-8 encoded bytestring.
    """

    @staticmethod
    @abc.abstractmethod
    def deserialize(record: Record, mapper: Type[BaseMapper[Record]]) -> bytes:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.

        Args:
            record: Some concrete record instance that inherits from BaseRecord.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed in.

        Returns:
            A bytestring of the data encoded by the specific Deserializer.
        """
        raise NotImplementedError

    @classmethod
    def deserialize_to_file(
        cls, record: Record, mapper: Type[BaseMapper[Record]], file_object: IO[bytes]
    ) -> None:
        """
        A convenience method that maps the record with the passed in mapper and
        writes it to a file object.

        Args:
            record: Some concrete record instance that inherits from BaseRecord.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed in.
            file_object: Some file-like object that can be read from. This
                includes io.BytesIO and file objects opened in byte mode.

        Raises:
            ValueError: An error has occured while doing I/O operations.
        """
        data = cls.deserialize(record, mapper)
        file_object.write(data)
