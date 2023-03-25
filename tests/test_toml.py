# -*- coding: utf-8 -*-
import ast
import io
from typing import Any, TypeVar

from serde_components.mappers import BaseMapper
from serde_components.serializers import TomlSerializer
from serde_components.deserializers import TomlDeserializer

T = TypeVar('T')


class Record:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name


class Mapper(BaseMapper):
    @staticmethod
    def map_serialize(record: Any) -> bytes:
        rv = {}
        if record.name:
            rv['name'] = record.name
        if record.age:
            rv['age'] = record.age

        return str(rv).encode('utf-8')

    @staticmethod
    def map_deserialize(record: Record, data: bytes) -> Record:
        _data = ast.literal_eval(data.decode('utf-8'))
        age = _data.get('age')
        if isinstance(age, str):
            try:
                record.age = int(age)
            except:
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


def test_toml_serializer():
    t = Record(name='testName', age=10)
    toml_data = TomlSerializer.serialize(t, Mapper).decode()

    assert toml_data == 'name = "testName"\nage = 10\n'


def test_toml_serializer_to_file1():
    t = Record(name='TestNameToml', age=10)
    file_object = io.BytesIO(b'')
    TomlSerializer.serialize_to_file(t, Mapper, file_object)

    with open('tests/data/toml/record1.toml', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_toml_serializer_to_file2():
    t = Record(name=None, age=None)
    file_object = io.BytesIO(b'')
    TomlSerializer.serialize_to_file(t, Mapper, file_object)
    golden_bytes = b''

    assert file_object.getvalue() == golden_bytes


def test_toml_serializer_to_file3():
    t = Record(name=100, age='TestNameToml')
    file_object = io.BytesIO(b'')
    TomlSerializer.serialize_to_file(t, Mapper, file_object)

    with open('tests/data/toml/record3.toml', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_toml_deserializer():
    t = Record(name='', age=0)
    toml_data = b'age = 10\nname = "testName"\n'
    TomlDeserializer.deserialize(t, Mapper, toml_data)
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_toml_deserializer_from_filebuffer():
    t = Record(name='', age=0)
    file_object = io.BytesIO(b'age = 10\nname = "testName"\n')
    TomlDeserializer.deserialize_from_file(t, Mapper, file_object)
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_toml_deserializer_actual_file1():
    with open('tests/data/toml/record1.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name='TestFileName', age=100)

    assert record, golden_record


def test_toml_deserializer_actual_file2():
    with open('tests/data/toml/record2.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=None, age=None)

    assert record, golden_record


def test_toml_deserializer_actual_file3():
    with open('tests/data/toml/record3.toml', 'rb') as file_object:
        record = Record(name='', age=0)
        TomlDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=10, age='TestFileName')

    assert record, golden_record
