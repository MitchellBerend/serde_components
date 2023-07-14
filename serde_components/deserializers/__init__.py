# -*- coding: utf-8 -*-
from typing import TypeVar
from .base import BaseDeserializer
from .csv_deserializer import CsvDeserializer
from .json_deserializer import JsonDeserializer
from .toml_deserializer import TomlDeserializer

D = TypeVar('D', bound=BaseDeserializer)
