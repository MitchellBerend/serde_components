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


# def test_csv_serializer():
#     data = [Record(name='testName', age=i) for i in range(10)]
#     csv_data = CsvSerializer.serialize(data, Mapper).decode()
#     with open('tests/data/csv/record1.csv', 'r') as golden_file_object:
#         golden_bytes = golden_file_object.read()[:-1]
#
#     assert csv_data == golden_bytes
#
#
# def test_csv_serializer_to_file():
#     data = [Record(name='testName', age=i) for i in range(10)]
#     file_object = io.BytesIO(b'')
#     CsvSerializer.serialize_to_file(data, Mapper, file_object)
#     with open('tests/data/csv/record1.csv', 'rb') as golden_file_object:
#         golden_bytes = golden_file_object.read()[:-1]
#
#     assert file_object.getvalue() == golden_bytes
#
#
# def test_csv_deserializer():
#     with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
#         data = golden_file_object.read()[:-1]
#     records = [Record(name='aaa', age=i + 100) for i in range(10)]
#     records = CsvDeserializer.deserialize(records, Mapper, data)
#     golden_records = [Record(name='testName', age=i) for i in range(10)]
#
#     assert records == golden_records
#
#
# def test_csv_deserializer_from_filebuffer():
#     with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
#         data = golden_file_object.read()[:-1]
#     file_object = io.BytesIO(data)
#     records = [Record(name='aaa', age=i + 100) for i in range(10)]
#     records = CsvDeserializer.deserialize_from_file(records, Mapper, file_object)
#     golden_records = [Record(name='testName', age=i) for i in range(10)]
#
#     assert records == golden_records
