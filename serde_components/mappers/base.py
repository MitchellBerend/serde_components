# -*- coding: utf-8 -*-
import abc
from typing import Generic, Type, TypeVar, Union


T = TypeVar('T')
RKind = Union[T, Type[T]]


class BaseMapper(abc.ABC, Generic[T]):
    """
    This class defines the interface that is required in order to use a derived
    class as a mapper object. It is technically possible to implement a class
    without inheriting from this base class, but the type checker will complain
    about it.
    """

    @staticmethod
    @abc.abstractmethod
    def map_deserialize(record: T) -> bytes:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def map_serialize(record: RKind[T], data: bytes) -> T:
        raise NotImplementedError
