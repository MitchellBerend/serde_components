# -*- coding: utf-8 -*-
import ast
import io
from typing import Any, TypeVar

from serde_components.mappers import BaseMapper
from serde_components.serializers import CsvSerializer, JsonSerializer
from serde_components.deserializers import CsvDeserializer, JsonDeserializer

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
        return str(
            {
                'age': record.age,
                'name': record.name,
            }
        ).encode('utf-8')

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


def test_json_serializer():
    t = Record(name='testName', age=10)
    json_data = JsonSerializer.serialize(t, Mapper).decode()

    assert json_data == "{\"age\": 10, \"name\": \"testName\"}"


def test_json_serializer_to_file1():
    t = Record(name='TestFileName', age=100)
    file_object = io.BytesIO(b'')
    JsonSerializer.serialize_to_file(t, Mapper, file_object)

    with open('tests/data/json/record1.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_serializer_to_file2():
    t = Record(name=None, age=None)
    file_object = io.BytesIO(b'')
    JsonSerializer.serialize_to_file(t, Mapper, file_object)
    golden_bytes = b'{"age": null, "name": null}'

    assert file_object.getvalue() == golden_bytes


def test_json_serializer_to_file3():
    t = Record(name=100, age='TestFileName')
    file_object = io.BytesIO(b'')
    JsonSerializer.serialize_to_file(t, Mapper, file_object)

    with open('tests/data/json/record3.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_deserializer():
    t = Record(name='', age=0)
    json_data = b'"{\'age\': 10, \'name\': \'testName\'}"'
    JsonDeserializer.deserialize(t, Mapper, json_data)
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_json_deserializer_from_filebuffer():
    t = Record(name='', age=0)
    file_object = io.BytesIO(b'"{\'age\': 10, \'name\': \'testName\'}"')
    JsonDeserializer.deserialize_from_file(t, Mapper, file_object)
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_json_deserializer_actual_file1():
    with open('tests/data/json/record1.json', 'rb') as file_object:
        record = Record(name='', age=0)
        JsonDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name='TestFileName', age=100)

    assert record, golden_record


def test_json_deserializer_actual_file2():
    with open('tests/data/json/record2.json', 'rb') as file_object:
        record = Record(name='', age=0)
        JsonDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=None, age=None)

    assert record, golden_record


def test_json_deserializer_actual_file3():
    with open('tests/data/json/record3.json', 'rb') as file_object:
        record = Record(name='', age=0)
        JsonDeserializer.deserialize_from_file(record, Mapper, file_object)
        golden_record = Record(name=10, age='TestFileName')

    assert record, golden_record
