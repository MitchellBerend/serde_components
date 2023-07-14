# -*- coding: utf-8 -*-
import ast
import csv
import io
from typing import Iterable, Type

from serde_components.deserializers import CsvDeserializer
from serde_components.mappers import BaseMapper
from serde_components.record import BaseRecord, Record
from serde_components.serializers import CsvSerializer, BaseSerializer


class ConcreteRecord(BaseRecord):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name


class Mapper(BaseMapper):
    @staticmethod
    def map_serialize(record: ConcreteRecord) -> bytes:  # type: ignore
        return str(
            {
                'age': record.age,
                'name': record.name,
            }
        ).encode('utf-8')

    @staticmethod
    def map_deserialize(record: ConcreteRecord, data: bytes) -> ConcreteRecord:  # type: ignore
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


class TsvSerializer(BaseSerializer):
    @staticmethod
    def serialize(records: Iterable[Record], mapper: Type[BaseMapper]) -> bytes:
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
            b_data: bytes = mapper.map_serialize(record)
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
    data = ast.literal_eval(Mapper.map_serialize(t).decode('utf-8'))
    golden_data = {
        'age': 10,
        'name': 'testName',
    }

    assert data == golden_data


def test_csv_serializer():
    data = [ConcreteRecord(name='testName', age=i) for i in range(10)]
    csv_data = CsvSerializer.serialize(data, Mapper).decode()
    with open('tests/data/csv/record1.csv', 'r') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert csv_data == golden_bytes


def test_csv_serializer_to_file():
    data = [ConcreteRecord(name='testName', age=i) for i in range(10)]
    file_object = io.BytesIO(b'')
    CsvSerializer.serialize_to_file(data, Mapper, file_object)
    with open('tests/data/csv/record1.csv', 'rb') as golden_file_object:
        golden_bytes = golden_file_object.read()[:-1]

    assert file_object.getvalue() == golden_bytes


def test_csv_deserializer():
    with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
        data = golden_file_object.read()[:-1]
    records = [ConcreteRecord(name='aaa', age=i + 100) for i in range(10)]
    records = CsvDeserializer.deserialize(records, Mapper, data)
    golden_records = [ConcreteRecord(name='testName', age=i) for i in range(10)]

    assert records == golden_records


def test_csv_deserializer_from_filebuffer():
    with open('tests/data/csv/record2.csv', 'rb') as golden_file_object:
        data = golden_file_object.read()[:-1]
    file_object = io.BytesIO(data)
    records = [ConcreteRecord(name='aaa', age=i + 100) for i in range(10)]
    records = CsvDeserializer.deserialize_from_file(
        records,
        Mapper,
        file_object,
    )
    golden_records = [ConcreteRecord(name='testName', age=i) for i in range(10)]

    assert records == golden_records
