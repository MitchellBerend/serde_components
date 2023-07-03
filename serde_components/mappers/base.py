# -*- coding: utf-8 -*-
import abc

from ..record import BaseRecord


class BaseMapper(metaclass=abc.ABCMeta):
    """
    This class defines the interface that is required in order to use a derived
    class as a mapper object. It is technically possible to implement a class
    without inheriting from this base class, but the type checker will complain
    about it.
    """

    @staticmethod
    @abc.abstractmethod
    def map_serialize(record: BaseRecord) -> bytes:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def map_deserialize(record: BaseRecord, data: bytes) -> BaseRecord:
        raise NotImplementedError
