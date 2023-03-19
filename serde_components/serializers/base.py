import abc
from typing import Any, Type, IO

from ..mappers import BaseMapper


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    This base class defines the interface that all serializers must implement.
    All methods that require implementation are marked with the
    @abc.abstractmethod decorator.

    Because this base does not know about the derived serializers desired
    format, everything string like is passed as a utf-8 encoded bytestring.
    """

    @staticmethod
    @abc.abstractmethod
    def serialize(record: Any, mapper: Type[BaseMapper]) -> bytes:
        """
        This method is the main way to interact with an instance of a class
        derived from this base.
        """
        raise NotImplementedError

    @classmethod
    def serialize_to_file(cls, record: Any, mapper: Type[BaseMapper], file_object: IO[bytes]) -> None:
        """
        A convenience method that maps the record with the passed in mapper and
        writes it to a file object.
        """
        data = cls.serialize(record, mapper)
        file_object.write(data)
