# -*- coding: utf-8 -*-
import ast
import io
import sys
from typing import Any, TypeVar

import pytest

from serde_components.mappers import BaseMapper
from serde_components.deserializers import TomlDeserializer
from serde_components.record import BaseRecord


T = TypeVar('T')


class Record(BaseRecord):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name


class Mapper(BaseMapper):
    @staticmethod
    def map_serialize(record: Record) -> bytes:  # type: ignore
        rv = {}
        if record.name:
            rv['name'] = record.name
        if record.age:
            rv['age'] = record.age

        return str(rv).encode('utf-8')

    @staticmethod
    def map_deserialize(record: Record, data: bytes) -> Record:  # type: ignore
        _data = ast.literal_eval(data.decode('utf-8'))
        age = _data.get('age')
        if isinstance(age, str):
            try:
                record.age = int(age)
            except:  # noqa
                record.age = age
        if isinstance(age, int):
            record.age = age
        record.name = _data.get('name')

        return record


def test_general_mapper():
    t = Record(name='testName', age=10)
    data = ast.literal_eval(Mapper.map_serialize(t).decode('utf-8'))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_toml_deserializer():
    t = Record(name='', age=0)
    toml_data = b'age = 10\nname = "testName"\n'
    if sys.version_info.minor < 11:
        with pytest.raises(ImportError):
            TomlDeserializer.deserialize(t, Mapper, toml_data)
    else:
        TomlDeserializer.deserialize(t, Mapper, toml_data)
        golden_record = Record(name='testName', age=10)

        assert t == golden_record


def test_toml_deserializer_from_filebuffer():
    t = Record(name='', age=0)
    file_object = io.BytesIO(b'age = 10\nname = "testName"\n')
    if sys.version_info.minor < 11:
        with pytest.raises(ImportError):
            TomlDeserializer.deserialize_from_file(t, Mapper, file_object)
    else:
        TomlDeserializer.deserialize_from_file(t, Mapper, file_object)
        golden_record = Record(name='testName', age=10)

        assert t == golden_record


def test_toml_deserializer_actual_file1():
    with open('tests/data/toml/record1.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                TomlDeserializer.deserialize_from_file(
                    record,
                    Mapper,
                    file_object,
                )
        else:
            TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name='TestFileName', age=100)

    assert record, golden_record


def test_toml_deserializer_actual_file2():
    with open('tests/data/toml/record2.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                TomlDeserializer.deserialize_from_file(
                    record,
                    Mapper,
                    file_object,
                )
        else:
            TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=None, age=None)

    assert record, golden_record


def test_toml_deserializer_actual_file3():
    with open('tests/data/toml/record3.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                TomlDeserializer.deserialize_from_file(
                    record,
                    Mapper,
                    file_object,
                )
        else:
            TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=10, age='TestFileName')

    assert record, golden_record
