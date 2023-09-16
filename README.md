[![codecov](https://codecov.io/gh/MitchellBerend/serde_components/branch/master/graph/badge.svg?token=Yh8LDG6KTt)](https://codecov.io/gh/MitchellBerend/serde_components)

Table of content
---

- [Serde components](#serde-components)
- [Implementation of custom components](#implementation-of-custom-components)
- [Examples](#examples)
- [Motivation](#motivation)

# Serde components

This library aims to provide pluggable components that handle the input,
transformation and output of custom classes or objects. It implements some
components and defines an interface to let custom ones interact with them. There
are 3 types of components that are currently defined.

 - DeSerializers
 - Serializers
 - Mappers

## Deserializers

Deserializers handle the input of a file format to a unspecified data structure.
Some file formats like json will map directly to a file format in python, but
this might not be the case for all file formats. Make sure to read the
documentation of the specific deserializer to find what data structure it
produces.

## Serializers

Serializers handle the output of a file format from a unspecified data
structure. Some data structures map to a file format nicely, for example a dict
to a json object. Some file formats might expect a very specific structure like
a csv that expects a list of dicts that all have the same keys. Make sure to
read the documentation of the specific serializer to find what limits there
are in terms of data structures.

## Mappers

Mappers are there to take a data structure and apply it on a given class or
object, or to take a given class or object and procude a data structure.

# Implementation of custom components

There are certain components that are ready to be used as is. These are all
serializers or deserializers. The common pattern in this library is that a
(de)serializer will take in a record, mapper and maybe some data, which then
will produce the desired outcome.

This way changing from json to toml will be a simple serializer swap without
touching the rest of the code.

Caution should be taken when the data structure that the deserializer or
serializer produes is not the same. A json serializer will not produce the same
data structure as the csv deserializer.

This library does not contain (de)serializers that depend on non standard
library provided modules and that is a conscious choice. It should be up to the
consumer of this library to decide if they want to use one dependency over
another (or none at all). This does however mean that a lot of common file types
are not supported out of the box.

# Examples

```python
import ast
import io
from typing import Iterable, Any

from serde_components.mappers import BaseMapper
from serde_components.record import BaseRecord
from serde_components.serializers import JsonSerializer, BaseSerializer


class Record(BaseRecord):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name


# This mapper does not take BaseRecord, since this mapper is specific to the
# concrete Record defined above. It's probably a good idea to give your own
# implementations a proper name.
class Mapper(BaseMapper):
    @staticmethod
    def map_serialize(record: Record) -> bytes:
        return str(
            {
                'age': record.age,
                'name': record.name,
            }
        ).encode('utf-8')

    @staticmethod
    def map_deserialize(record: Record, data: bytes) -> Record:
        _data = ast.literal_eval(data)
        record.age = int(_data.get('age'))
        record.name = _data.get('name')

        return record

# Since the CsvSerializer only produces comma separated data, this exmaple
# also includes a TsvSerializer.
class TsvSerializer(BaseSerializer):
    @staticmethod
    def serialize(records: Iterable[R], mapper: Type[BaseMapper]) -> bytes:
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


if __name__ == '__main__':
    records [
        Record(name='testName', age=index) for index in range(10)
    ]

    # Since these components are made to be almost freely interchangable, this
    # all works without any problems. The only difference exist in the file
    # format that needs to be exported to. It does not make sense to have a
    # single csv or tsv file for every record. Since mappers only map one record
    # to a certain data structure, the serializer needs to handle more than one
    # case.
    json_data = JsonSerializer.serialize(records[0], Mapper).decode()
    tsv_data = TsvSerializer.serialize(records, Mapper).decode()
    csv_data = CsvSerializer.serialize(records, Mapper).decode()

    assert json_data == '"{\'age\': 1, \'name\': \'testName\'}"'
```

# Motivation

This serves as an example, practice and production case. In the orm world, I
have personally come across many situations where one model needed to be mapped
to a different structure all together. Whether this was a json object for rest a
api or a csv file for some flatfile interface. This library aims to standardize
the import transformation and export operations.
