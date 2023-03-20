# -*- coding: utf-8 -*-
import abc
from typing import Any, TypeVar

T = TypeVar('T')


class BaseMapper(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def map_serialize(record: Any) -> bytes:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def map_deserialize(record: T, data: bytes) -> T:
        raise NotImplementedError
