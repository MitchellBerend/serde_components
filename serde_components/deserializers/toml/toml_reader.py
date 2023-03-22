# -*- coding: utf-8 -*-
################################################################################
# !Disclaimer!
# Do not depend on this class if you aren't implementing anything in this
# library's internals. This class is considered a private class. There is no
# guarantee this class will function the same, or even exist at any point in the
# future.
################################################################################


from typing import Any, Dict


class InternalTomlLib:
    """
    This class represents the standard library's tomllib, which was added in
    3.11. Since this library supports python versions before 3.11, there needs
    to be some other implementation that can take it's place
    """

    @staticmethod
    def _read_till_sep(s, sep_list):
        rv = []
        placeholder = ''
        for letter in s:
            if letter in sep_list:
                rv.append(placeholder)
                placeholder = ''
            else:
                placeholder += letter
        return [r for r in rv if r and r not in sep_list]

    @staticmethod
    def _type_checker(s):
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

    @staticmethod
    def loads(data: str):
        sep_list = [' ', '\n']
        rv = {}
        tokens = InternalTomlLib._read_till_sep(data, sep_list)
        placeholder: Dict[str, Any] = {}

        for token in tokens:
            if len(placeholder) < 3:
                if InternalTomlLib._type_checker(token) == 'str':
                    placeholder[InternalTomlLib._type_checker(token)] = token[1:-1]
                else:
                    placeholder[InternalTomlLib._type_checker(token)] = token
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
                if InternalTomlLib._type_checker(token) == 'str':
                    placeholder[InternalTomlLib._type_checker(token)] = token[1:-1]
                else:
                    placeholder[InternalTomlLib._type_checker(token)] = token

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
