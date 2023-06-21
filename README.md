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

 - Serializers
 - Deserializers
 - Mappers

## Serializers

Serializers handle the input of a file format to a unspecified data structure.
Some file formats like json will map directly to a file format in python, but
this might not be the case for all file formats. Make sure to read the
documentation of the specific serializer to find what data structure it
produces.

## Deserializers

Deserializers handle the output of a file format from a unspecified data
structure. Some data structures map to a file format nicely, for example a dict
to a json object. Some file formats might expect a very specific structure like
a csv that expects a list of dicts that all have the same keys. Make sure to
read the documentation of the specific deserializer to find what limits there
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

Caution should be taken when the data structure that the serializer or
deserializer produes is not the same. A json serializer will not produce the
same data structure as the csv serializer.

This library does not contain (de)serializers that depend on non standard
library provided modules and that is a conscious choice. It should be up to the
consumer of this library to decide if they want to use one dependency over
another (or none at all). This does however mean that a lot of common file types
are not supported out of the box.



# Examples

```python
import ast
import io
from typing import Any

from serde_components.mappers import BaseMapper
from serde_components.serializers import JsonSerializer

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
        _data = ast.literal_eval(data)
        record.age = int(_data.get('age'))
        record.name = _data.get('name')

        return record

if __name__ == '__main__':
    record = Record(name='testName', age=10)
    json_data = JsonSerializer.serialize(record, Mapper).decode()

    assert json_data == '"{\'age\': 10, \'name\': \'testName\'}"'
```

# Motivation

This serves as an example, practice and production case. In the orm world, I
have personally come across many situations where one model needed to be mapped
to a different structure all together. Whether this was a json object for rest a
api or a csv file for some flatfile interface. This library aims to standardize
the import transformation and export operations.
