# -*- coding: utf-8 -*-
import ast
import io
import sys
from typing import Type, Union

import pytest

from serde_components.mappers import BaseMapper
from serde_components.serializers import TomlSerializer

from .conftest import ConcreteRecord

Alias = Union[ConcreteRecord, Type[ConcreteRecord]]


class Mapper(BaseMapper[ConcreteRecord]):
    @staticmethod
    def map_deserialize(record: Alias) -> bytes:
        assert isinstance(record, ConcreteRecord)
        rv = {}
        if record.name:
            rv['name'] = record.name
        if record.age:
            rv['age'] = record.age

        return str(rv).encode('utf-8')

    @staticmethod
    def map_serialize(record: Alias, data: bytes) -> ConcreteRecord:
        assert isinstance(record, ConcreteRecord)
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


def test_general_mapper(record):
    data = ast.literal_eval(Mapper.map_deserialize(record).decode('utf-8'))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_toml_deserializer(record):
    toml_data = b'age = 10\nname = "testName"\n'
    if sys.version_info.minor < 11:
        with pytest.raises(ImportError):
            TomlSerializer.serialize(record, Mapper, toml_data)
    else:
        TomlSerializer.serialize(record, Mapper, toml_data)
        golden_record = ConcreteRecord(name='testName', age=10)

        assert record == golden_record


def test_toml_factory_deserializer(record):
    toml_data = b'age = 10\nname = "testName"\n'
    if sys.version_info.minor < 11:
        with pytest.raises(ImportError):
            record = TomlSerializer.serialize(
                ConcreteRecord,
                Mapper,
                toml_data,
            )
    else:
        record = TomlSerializer.serialize(
            ConcreteRecord,
            Mapper,
            toml_data,
        )
        golden_record = ConcreteRecord(name='testName', age=10)

        assert record == golden_record


def test_toml_deserializer_from_filebuffer(record):
    file_object = io.BytesIO(b'age = 10\nname = "testName"\n')
    if sys.version_info.minor < 11:
        with pytest.raises(ImportError):
            TomlSerializer.serialize_from_file(
                record,
                Mapper,
                file_object,
            )
    else:
        TomlSerializer.serialize_from_file(record, Mapper, file_object)
        golden_record = ConcreteRecord(name='testName', age=10)

        assert record == golden_record


def test_toml_serializer_actual_file1(record):
    with open('tests/data/toml/record1.toml', 'rb') as file_object:
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                TomlSerializer.serialize_from_file(
                    ConcreteRecord,
                    Mapper,
                    file_object,
                )
        else:
            TomlSerializer.serialize_from_file(
                ConcreteRecord,
                Mapper,
                file_object,
            )
        golden_record = ConcreteRecord(name='testName', age=10)

    assert record == golden_record


def test_toml_serializer_actual_file2():
    with open('tests/data/toml/record2.toml', 'rb') as file_object:
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                record = TomlSerializer.serialize_from_file(
                    ConcreteRecord,
                    Mapper,
                    file_object,
                )
            return
        else:
            record = TomlSerializer.serialize_from_file(
                ConcreteRecord,
                Mapper,
                file_object,
            )
        golden_record = ConcreteRecord(name=None, age=None)

    assert record == golden_record


def test_toml_serializer_actual_file3():
    record = ConcreteRecord(name='test', age=123)
    with open('tests/data/toml/record3.toml', 'rb') as file_object:
        if sys.version_info.minor < 11:
            with pytest.raises(ImportError):
                TomlSerializer.serialize_from_file(
                    record,
                    Mapper,
                    file_object,
                )
            return
        else:
            TomlSerializer.serialize_from_file(
                record,
                Mapper,
                file_object,
            )
        golden_record = ConcreteRecord(name=10, age='testName')

    assert record == golden_record
