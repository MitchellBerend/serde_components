# -*- coding: utf-8 -*-
import abc
from typing import Generic, IO, Type, TypeVar, Union

from ..mappers import BaseMapper

T = TypeVar('T')
RKind = Union[T, Type[T]]


class BaseSerializer(abc.ABC, Generic[T]):
    """
    This base class defines the interface that all serializers must
    implement. All methods that require implementation are marked with the
    @abc.abstractmethod decorator.

    Because this base does not know about the derived serializers desired
    format, everything string like is passed as a utf-8 encoded bytestring.
    """

    @staticmethod
    @abc.abstractmethod
    def serialize(record: RKind[T], mapper: Type[BaseMapper[T]], data: bytes) -> T:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.

        Args:
            record: Some concrete record instance or a factory method that
                creates an instance of a record when called.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Serializer.

        Returns:
            The passed record with data mapped from the data.
        """
        raise NotImplementedError

    @classmethod
    def serialize_from_file(
        cls,
        record: RKind[T],
        mapper: Type[BaseMapper[T]],
        file_object: IO[bytes],
    ) -> T:
        """
        A convenience method that reads data from a file object and maps it to
        the record with the passed in mapper.

        Args:
            record: Some concrete record instance or a factory method that
                creates an instance of a
                record when called.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Serializer.
            file_object: Some file-like object that can be read from. This
                includes io.BytesIO and file objects opened in byte mode.

        Returns:
            The passed record with data mapped from the data.

        Raises:
            ValueError: An error has occured while doing I/O operations.
        """
        data = file_object.read()
        return cls.serialize(record, mapper, data)
