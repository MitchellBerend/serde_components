# -*- coding: utf-8 -*-
import inspect
from typing import IO, Type, TypeVar, Union
import sys

from .base import BaseSerializer
from ..mappers import BaseMapper

T = TypeVar('T')
RKind = Union[T, Type[T]]
PYTHON_VERSION_ERROR = 'Your python version does not support this component'


if sys.version_info.minor >= 11:
    import tomllib  # type:ignore


class TomlSerializer(BaseSerializer[T]):
    @staticmethod
    def serialize(
        record: RKind[T],
        mapper: Type[BaseMapper[T]],
        data: bytes,
    ) -> T:
        """
        This method is only available in python versions 3.11 and later.

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

        Raises:
            NameError: Tomllib is not available on the system. This class is
                only supported on python versions 3.11 and later.
        """
        # tomllib.loads does not take in bytestrings like json.loads does
        _data: str = data.decode('utf-8')
        _rv = None

        try:
            toml = tomllib.loads(_data)
        except NameError:
            raise ImportError(PYTHON_VERSION_ERROR)

        toml_data: bytes = str(toml).encode('utf-8')

        if inspect.isclass(record):
            _record = record()
            _rv = mapper.map_serialize(_record, toml_data)
        else:
            _rv = mapper.map_serialize(record, toml_data)

        return _rv

    @classmethod
    def serialize_from_file(
        cls,
        record: RKind[T],
        mapper: Type[BaseMapper[T]],
        file_object: IO[bytes],
    ) -> T:
        """
        This method is only available in python versions 3.11 and later.

        Args:
            record: Some concrete record instance.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Serializer.

        Returns:
            The passed record with data mapped from the data.

        Raises:
            NameError: Tomllib is not available on the system. This class is
                only supported on python versions 3.11 and later.
            ValueError: An error has occured while doing I/O operations.
        """
        r = record
        m = mapper
        fo = file_object
        return super().serialize_from_file(r, m, fo)
