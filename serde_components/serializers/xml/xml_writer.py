# -*- coding: utf-8 -*-
################################################################################
# !Disclaimer!
# Do not depend on this class if you aren't implementing anything in this
# library's internals. This class is considered a private class. There is no
# guarantee this class will function the same, or even exist at any point in the
# future.
################################################################################


from typing import Any, Dict


class XmlWriter:
    @staticmethod
    def dumps(data: Dict[str, Any], indent=0) -> bytes:
        rv = ''
        for key, value in data.items():
            if not value:
                rv += XmlWriter._key_value(key, value, indent)
            elif isinstance(value, str):
                rv += XmlWriter._key_value(key, value, indent)
            elif isinstance(value, int):
                rv += XmlWriter._key_value(key, value, indent)
            elif isinstance(value, dict):
                _val = XmlWriter.dumps(value, indent=indent + 1).decode('utf-8')
                rv += f'{"  "*indent}<{key}>\n{str(_val)}</{key}>\n'
            else:
                raise NotImplementedError
        return rv.encode('utf-8')

    @staticmethod
    def _key_value(key: str, value: Any, indent: int) -> str:
        if not value:
            return f'{"  "*indent}<{key}/>\n'
        else:
            return f'{"  "*indent}<{key}>{str(value)}</{key}>\n'
