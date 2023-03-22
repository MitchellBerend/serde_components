# -*- coding: utf-8 -*-
################################################################################
# !Disclaimer!
# Do not depend on this class if you aren't implementing anything in this
# library's internals. This class is considered a private class. There is no
# guarantee this class will function the same, or even exist at any point in the
# future.
################################################################################


from typing import Any, Dict, List, Union


class InternalTomlLibWriter:
    """
    This class represents the standard library's tomllib, which was added in
    3.11. Since this library supports python versions before 3.11, there needs
    to be some other implementation that can take it's place.

    All the methods on this class are marked as staticmethods to mimick a
    library.
    """

    @staticmethod
    def _parse_data(data: Union[Dict[str, Any], List[Any]]) -> str:
        rv = ''

        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, str):
                    _val = f'"{val}"'
                elif isinstance(val, list):
                    _val = InternalTomlLibWriter._parse_data(val)
                elif isinstance(val, dict):
                    _val = InternalTomlLibWriter.second_dict_parse(val)
                else:
                    _val = f'{val}'
                rv += f'{key} = {_val}\n'

        elif isinstance(data, List):
            if not data:
                return '[]'
            _data = []
            for val in data:
                if isinstance(val, str):
                    _data.append(f'"{val}"')
                elif isinstance(val, dict):
                    _placeholder = InternalTomlLibWriter.second_dict_parse(val)
                    _data.append(_placeholder)
                else:
                    _data.append(str(val))
            return '[{}'.format(', '.join([r for r in _data])) + ']'

        return rv

    @staticmethod
    def second_dict_parse(data: Dict[str, Union[str, int, float]]) -> str:
        assert isinstance(data, dict)
        placeholder: List[str] = []

        for key, val in data.items():
            if isinstance(val, str):
                _rv = f'"{key}" = "{val}"'
                placeholder.append(_rv)
            elif isinstance(val, dict):
                _rv = InternalTomlLibWriter.second_dict_parse(val)
                placeholder.append(_rv)
            else:
                _rv = f'"{key}" = {val}'
                placeholder.append(_rv)

        return '{{ {} }}'.format(', '.join(placeholder))

    @staticmethod
    def dumps(data: Dict[str, Any]) -> bytes:
        data_str: str = InternalTomlLibWriter._parse_data(data)

        return data_str.encode('utf-8')
