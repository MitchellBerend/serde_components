# -*- coding: utf-8 -*-
import ast
import csv
import io
from typing import Iterable, Type

from serde_components.serializers import CsvSerializer
from serde_components.mappers import BaseMapper
from serde_components.deserializers import CsvDeserializer, BaseDeserializer


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


class TsvDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(
        records: Iterable[ConcreteRecord],
        mapper: Type[BaseMapper[ConcreteRecord]],
    ) -> bytes:
        """
        This method takes in a iterable over the records and maps the data from
        a to a tsv format. It takes an iterable since a tsv will contain rows
        which should correspond with a single record.

        This class takes a different type than the BaseSerializer, it does not
        make sense for a tsv serializer to only map a single record. For this
        reason the type checking is ignored.
        """

        mapped_data = []
        for record in records:
            b_data: bytes = mapper.map_deserialize(record)
            data = b_data.decode('utf-8')
            mapped_data.append(ast.literal_eval(data))
        assert len(mapped_data) > 1

        keys = list(mapped_data[0].keys())
        file_object = io.StringIO('')

        writer = csv.DictWriter(
            file_object,
            fieldnames=keys,
            delimiter='t',
            dialect='unix',
        )
        writer.writeheader()
        for row in mapped_data:
            writer.writerow(row)

        return file_object.getvalue().encode('utf-8')


def test_general_mapper():
    t = ConcreteRecord(name='testName', age=10)
    data = ast.literal_eval(Mapper.map_deserialize(t).decode('utf-8'))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_csv_deserializer():
    data = [ConcreteRecord(name='testName', age=i) for i in range(10)]
    csv_data = CsvDeserializer.deserialize(data, Mapper).decode()
    with open('tests/data/csv/record1.csv', 'r') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert csv_data == golden_bytes


def test_csv_deserializer_to_file():
    data = [ConcreteRecord(name='testName', age=i) for i in range(10)]
    file_object = io.BytesIO(b'')
    CsvDeserializer.deserialize_to_file(data, Mapper, file_object)
    with open('tests/data/csv/record1.csv', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_csv_serializer():
    with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
        data = golden_file_object.read()[:-1]
    records = [ConcreteRecord(name='aaa', age=i + 100) for i in range(10)]
    records = CsvSerializer.serialize(records, Mapper, data)
    golden_records = [ConcreteRecord(name='testName', age=i) for i in range(10)]

    assert records == golden_records


def test_factory_csv_serializer():
    with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
        data = golden_file_object.read()[:-1]
    records = CsvSerializer.serialize(ConcreteRecord, Mapper, data)
    golden_records = [ConcreteRecord(name='testName', age=i) for i in range(10)]

    assert records == golden_records


def test_csv_serializer_from_filebuffer():
    with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
        data = golden_file_object.read()[:-1]
    file_object = io.BytesIO(data)
    records = [ConcreteRecord(name='aaa', age=i + 100) for i in range(10)]
    records = CsvSerializer.serialize_from_file(
        records,
        Mapper,
        file_object,
    )
    golden_records = [ConcreteRecord(name='testName', age=i) for i in range(10)]

    assert records == golden_records
