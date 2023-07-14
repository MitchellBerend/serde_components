# -*- coding: utf-8 -*-
import abc
from typing import Generic, IO, Iterable, Type

from ..mappers import BaseMapper
from ..record import Record


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
        record: Record, mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.
        """
        raise NotImplementedError

    @classmethod
    def deserialize_from_file(
        cls,
        record: Record,
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Record:
        """
        A convenience method that reads data from a file object and maps it to
        the record with the passed in mapper.
        """
        data = file_object.read()
        return cls.deserialize(record, mapper, data)
