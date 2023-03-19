# -*- coding: utf-8 -*-
import io
from typing import Any, TypeVar

from serde_components.mappers import BaseMapper
from serde_components.serializers import CsvSerializer, JsonSerializer
from serde_components.deserializers import CsvDeserializer, JsonDeserializer

T = TypeVar('T')

CSV_GOLDEN_DATA = '"age","name"\n"0","testName"\n"1","testName"\n"2","testName"\n"3","testName"\n"4","testName"\n"5","testName"\n"6","testName"\n"7","testName"\n"8","testName"\n"9","testName"\n'


class Record:
    def __init__(self, name: str, age: int):
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
        _data = eval(data)
        record.age = int(_data.get('age'))
        record.name = _data.get('name')

        return record


def test_general_mapper():
    t = Record(name='testName', age=10)
    data = eval(Mapper.map_serialize(t))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_json_serializer():
    t = Record(name='testName', age=10)
    json_data = JsonSerializer.serialize(t, Mapper).decode()

    assert json_data == '"{\'age\': 10, \'name\': \'testName\'}"'


def test_json_serializer_to_file():
    t = Record(name='testName', age=10)
    file_object = io.BytesIO(b'')
    JsonSerializer.serialize_to_file(t, Mapper, file_object)

    assert file_object.getvalue() == '"{\'age\': 10, \'name\': \'testName\'}"'.encode()


def test_json_deserializer():
    t = Record(name='', age=0)
    json_data = '"{\'age\': 10, \'name\': \'testName\'}"'
    JsonDeserializer.deserialize(t, Mapper, json_data.encode('utf-8'))
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_json_deserializer_from_file():
    t = Record(name='', age=0)
    file_object = io.BytesIO(b'"{\'age\': 10, \'name\': \'testName\'}"')
    JsonDeserializer.deserialize_from_file(t, Mapper, file_object)
    golden_record = Record(name='testName', age=10)

    assert t == golden_record


def test_csv_serializer():
    data = [Record(name='testName', age=i) for i in range(10)]
    csv_data = CsvSerializer.serialize(data, Mapper).decode()

    assert csv_data == CSV_GOLDEN_DATA


def test_csv_serializer_to_file():
    data = [Record(name='testName', age=i) for i in range(10)]
    file_object = io.BytesIO(b'')
    CsvSerializer.serialize_to_file(data, Mapper, file_object)

    assert file_object.getvalue() == CSV_GOLDEN_DATA.encode('utf-8')


def test_csv_deserializer():
    data = CSV_GOLDEN_DATA.encode('utf-8')
    records = [Record(name='aaa', age=i + 100) for i in range(10)]
    records = CsvDeserializer.deserialize(records, Mapper, data)
    golden_records = [Record(name='testName', age=i) for i in range(10)]

    assert records == golden_records


def test_csv_deserializer_from_file():
    file_object = io.BytesIO(CSV_GOLDEN_DATA.encode('utf-8'))
    records = [Record(name='aaa', age=i + 100) for i in range(10)]
    records = CsvDeserializer.deserialize_from_file(records, Mapper, file_object)
    golden_records = [Record(name='testName', age=i) for i in range(10)]

    assert records == golden_records
