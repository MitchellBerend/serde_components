import abc
from typing import Type, TypeVar, IO

from ..mappers import BaseMapper

T = TypeVar('T')


class BaseDeserializer(metaclass=abc.ABCMeta):
    """
    This base class defines the interface that all deserializers must implement.
    All methods that require implementation are marked with the
    @abc.abstractmethod decorator.

    Because this base does not know about the derived deserializers desired
    format, everything string like is passed as a utf-8 encoded bytestring.
    """

    @staticmethod
    @abc.abstractmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.
        """
        raise NotImplementedError

    @classmethod
    def deserialize_from_file(cls, record: T, mapper: Type[BaseMapper], file_object: IO[bytes]) -> T:
        """
        A convenience method that reads data from a file object and maps it to
        the record with the passed in mapper.
        """
        data = file_object.getvalue()
        return cls.deserialize(record, mapper, data)
