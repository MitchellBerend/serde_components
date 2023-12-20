# -*- coding: utf-8 -*-
import ast
import io
from typing import Type, Union

from serde_components.serializers import JsonSerializer
from serde_components.mappers import BaseMapper
from serde_components.deserializers import JsonDeserializer

from .conftest import ConcreteRecord

Alias = Union[ConcreteRecord, Type[ConcreteRecord]]


class Mapper(BaseMapper[ConcreteRecord]):
    @staticmethod
    def map_deserialize(record: Alias) -> bytes:
        assert isinstance(record, ConcreteRecord)
        return str(
            {
                'age': record.age,
                'name': record.name,
            }
        ).encode('utf-8')

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


def test_json_deserializer(record):
    json_data = JsonDeserializer.deserialize(record, Mapper).decode()

    assert json_data == '{"age": 10, "name": "testName"}'


def test_json_deserializer_to_file1(record):
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(record, Mapper, file_object)

    with open('tests/data/json/record1.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_deserializer_to_file2():
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(
        ConcreteRecord(name=None, age=None),
        Mapper,
        file_object,
    )
    golden_bytes = b'{"age": null, "name": null}'

    assert file_object.getvalue() == golden_bytes


def test_json_deserializer_to_file3():
    file_object = io.BytesIO(b'')
    JsonDeserializer.deserialize_to_file(
        ConcreteRecord(name=10, age='testName'),
        Mapper,
        file_object,
    )

    with open('tests/data/json/record3.json', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_json_serializer(record):
    json_data = b'"{\'age\': 10, \'name\': \'testName\'}"'
    JsonSerializer.serialize(record, Mapper, json_data)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert record == golden_record


def test_json_factory_serializer():
    json_data = b'"{\'age\': 10, \'name\': \'testName\'}"'
    record = JsonSerializer.serialize(ConcreteRecord, Mapper, json_data)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert record == golden_record


def test_json_serializer_from_filebuffer(record):
    file_object = io.BytesIO(b'"{\'age\': 10, \'name\': \'testName\'}"')
    JsonSerializer.serialize_from_file(record, Mapper, file_object)
    golden_record = ConcreteRecord(name='testName', age=10)

    assert record == golden_record


def test_json_serializer_actual_file1(record):
    with open('tests/data/json/record1.json', 'rb') as file_object:
        JsonSerializer.serialize_from_file(record, Mapper, file_object)
        golden_record = ConcreteRecord(name='testName', age=10)

    assert record == golden_record


def test_json_serializer_actual_file2():
    with open('tests/data/json/record2.json', 'rb') as file_object:
        single_record = JsonSerializer.serialize_from_file(
            ConcreteRecord,
            Mapper,
            file_object,
        )
        golden_record = ConcreteRecord(name=None, age=None)

    assert single_record == golden_record


def test_json_serializer_actual_file3():
    with open('tests/data/json/record3.json', 'rb') as file_object:
        single_record = JsonSerializer.serialize_from_file(
            ConcreteRecord,
            Mapper,
            file_object,
        )
        golden_record = ConcreteRecord(name=10, age='testName')

    assert single_record == golden_record
