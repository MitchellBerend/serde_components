# -*- coding: utf-8 -*-
import ast
import io

from serde_components.serializers import JsonSerializer
from serde_components.mappers import BaseMapper
from serde_components.deserializers import JsonDeserializer


class ConcreteRecord:
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name


class Mapper(BaseMapper[ConcreteRecord]):
    @staticmethod
    def map_deserialize(record: ConcreteRecord) -> bytes:
        return str(
            {
                'age': record.age,
                'name': record.name,
            }
        ).encode('utf-8')

    @staticmethod
    def map_serialize(record: ConcreteRecord, data: bytes) -> ConcreteRecord:
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
    t = ConcreteRecord(name='testName', age=10)
    data = ast.literal_eval(Mapper.map_deserialize(t).decode('utf-8'))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_json_deserializer():
    t = ConcreteRecord(name='testName', age=10)
    json_data = JsonDeserializer.deserialize(t, Mapper).decode()

    assert json_data == '{"age": 10, "name": "testName"}'


def test_json_deserializer_to_file1():
    t = ConcreteRecord(name='TestFileName', age=100)
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(t, Mapper, file_object)

    with open('tests/data/json/record1.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_deserializer_to_file2():
    t = ConcreteRecord(name=None, age=None)
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(t, Mapper, file_object)
    golden_bytes = b'{"age": null, "name": null}'

    assert file_object.getvalue() == golden_bytes


def test_json_deserializer_to_file3():
    t = ConcreteRecord(name=100, age='TestFileName')
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(t, Mapper, file_object)

    with open('tests/data/json/record3.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_serializer():
    t = ConcreteRecord(name='', age=0)
    json_data = b'"{\'age\': 10, \'name\': \'testName\'}"'
    JsonSerializer.serialize(t, Mapper, json_data)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert t == golden_record


def test_json_factory_serializer():
    json_data = b'"{\'age\': 10, \'name\': \'testName\'}"'
    t = JsonSerializer.serialize(ConcreteRecord, Mapper, json_data)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert t == golden_record


def test_json_serializer_from_filebuffer():
    t = ConcreteRecord(name='', age=0)
    file_object = io.BytesIO(b'"{\'age\': 10, \'name\': \'testName\'}"')
    JsonSerializer.serialize_from_file(t, Mapper, file_object)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert t == golden_record


def test_json_serializer_actual_file1():
    with open('tests/data/json/record1.json', 'rb') as file_object:
        record = ConcreteRecord(name='', age=0)
        JsonSerializer.serialize_from_file(record, Mapper, file_object)
        golden_record = ConcreteRecord(name='TestFileName', age=100)

    assert record, golden_record


def test_json_serializer_actual_file2():
    with open('tests/data/json/record2.json', 'rb') as file_object:
        record = ConcreteRecord(name='', age=0)
        JsonSerializer.serialize_from_file(record, Mapper, file_object)
        golden_record = ConcreteRecord(name=None, age=None)

    assert record, golden_record


def test_json_serializer_actual_file3():
    with open('tests/data/json/record3.json', 'rb') as file_object:
        record = ConcreteRecord(name='', age=0)
        JsonSerializer.serialize_from_file(record, Mapper, file_object)
        golden_record = ConcreteRecord(name=10, age='TestFileName')

    assert record, golden_record
