# -*- coding: utf-8 -*-
import abc
from typing import Generic

from ..record import Record


class BaseMapper(abc.ABC, Generic[Record]):
    """
    This class defines the interface that is required in order to use a derived
    class as a mapper object. It is technically possible to implement a class
    without inheriting from this base class, but the type checker will complain
    about it.
    """

    @staticmethod
    @abc.abstractmethod
    def map_deserialize(record: Record) -> bytes:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def map_serialize(record: Record, data: bytes) -> Record:
        raise NotImplementedError
