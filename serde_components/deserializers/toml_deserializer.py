# -*- coding: utf-8 -*-
from typing import IO, Type
import sys

from .base import BaseDeserializer
from ..mappers import BaseMapper
from ..record import Record

PYTHON_VERSION_ERROR = 'Your python version does not support this component'


if sys.version_info.minor >= 11:
    import tomllib  # type: ignore


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(
        record: Record, mapper: Type[BaseMapper[Record]], data: bytes
    ) -> Record:
        """
        This method is only available in python versions 3.11 and later.

        Args:
            record: Some concrete record instance that inherits from BaseRecord.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed in.
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

        try:
            toml = tomllib.loads(_data)
        except NameError:
            raise ImportError(PYTHON_VERSION_ERROR)

        toml_data: bytes = str(toml).encode('utf-8')
        mapper.map_deserialize(record, toml_data)  # type:ignore

        return record

    @classmethod
    def deserialize_from_file(
        cls,
        record: Record,
        mapper: Type[BaseMapper[Record]],
        file_object: IO[bytes],
    ) -> Record:
        """
        This method is only available in python versions 3.11 and later.

        Args:
            record: Some concrete record instance that inherits from BaseRecord.
            mapper: Some concrete mapper class that inherits from BaseMapper,
                this mapper should be specific for the type of record passed in.
            data: Some bytestring that represents the record in a format
                specified by the concrete Deserializer.

        Returns:
            The passed record with data mapped from the data.

        Raises:
            NameError: Tomllib is not available on the system. This class is
                only supported on python versions 3.11 and later.
            ValueError: An error has occured while doing I/O operations.
        """
        return super().deserialize_from_file(record, mapper, file_object)
