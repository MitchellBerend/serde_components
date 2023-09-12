# -*- coding: utf-8 -*-
import inspect
from typing import IO, Type, Union
import sys

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record

RKind = Union[Record, Type[Record]]  # type:ignore
PYTHON_VERSION_ERROR = 'Your python version does not support this component'


if sys.version_info.minor >= 11:
    import tomllib  # type:ignore


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(
        record: RKind[Record],
        mapper: Type[BaseMapper[Record]],  # type:ignore
        data: bytes,
    ) -> Record:  # type:ignore
        """
        This method is only available in python versions 3.11 and later.

        Args:
            record: Some concrete record instance that inherits from
                BaseRecord or a factory method that creates an instance of a
                record when called.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed
                in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.

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
            _rv = mapper.map_deserialize(_record, toml_data)  # type:ignore
        else:
            _rv = mapper.map_deserialize(record, toml_data)  # type:ignore

        return _rv  # type:ignore

    @classmethod
    def deserialize_from_file(
        cls,
        record: RKind[Record],
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Record:  # type:ignore
        """
        This method is only available in python versions 3.11 and later.

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

        Raises:
            NameError: Tomllib is not available on the system. This class is
                only supported on python versions 3.11 and later.
            ValueError: An error has occured while doing I/O operations.
        """
        r = record
        m = mapper
        fo = file_object
        return super().deserialize_from_file(r, m, fo)  # type:ignore
