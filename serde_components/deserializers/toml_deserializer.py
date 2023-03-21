# -*- coding: utf-8 -*-
from typing import Type, TypeVar

from .base import BaseDeserializer
from ..mappers import BaseMapper

try:
    import tomllib
except ModuleNotFoundError:

    class tomllib:
        @staticmethod
        def loads(data: str):
            sep_list = [' ', '\n']

            def read_till_sep(s, sep_list):
                rv = []
                placeholder = ''
                for letter in s:
                    if letter in sep_list:
                        rv.append(placeholder)
                        placeholder = ''
                    else:
                        placeholder += letter
                return [r for r in rv if r and r not in sep_list]

            def type_checker(s):
                if s[0] == '"' and s[-1] == '"':
                    return 'str'
                elif s == '=':
                    return 'assignment'
                try:
                    if '.' in s:
                        float(s)
                        return 'float'
                    else:
                        int(s)
                        return 'int'
                except ValueError:
                    return 'label'

            rv = {}
            tokens = read_till_sep(data, sep_list)
            placeholder = {}
            for token in tokens:
                if len(placeholder) < 3:
                    if type_checker(token) == 'str':
                        placeholder[type_checker(token)] = token[1:-1]
                    else:
                        placeholder[type_checker(token)] = token
                else:
                    key = placeholder['label']
                    if 'str' in placeholder.keys():
                        value = placeholder.get('str')
                    elif 'float' in placeholder.keys():
                        value = float(placeholder['float'])
                    else:
                        value = int(placeholder['int'])
                    rv[key] = value
                    placeholder = {}
                    if type_checker(token) == 'str':
                        placeholder[type_checker(token)] = token[1:-1]
                    else:
                        placeholder[type_checker(token)] = token
            if len(placeholder) == 3:
                key = placeholder['label']
                if 'str' in placeholder.keys():
                    value = placeholder.get('str')
                elif 'float' in placeholder.keys():
                    value = float(placeholder['float'])
                else:
                    value = int(placeholder['int'])
                rv[key] = value
            return rv


T = TypeVar('T')


class TomlDeserializer(BaseDeserializer):
    @staticmethod
    def deserialize(record: T, mapper: Type[BaseMapper], data: bytes) -> T:
        # tomllib.loads does not take in bytestrings like json.loads does
        _data: str = data.decode('utf-8')
        toml = tomllib.loads(_data)
        toml_data: bytes = str(toml).encode('utf-8')
        mapper.map_deserialize(record, toml_data)

        return record
