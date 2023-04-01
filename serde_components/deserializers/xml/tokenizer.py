# -*- coding: utf-8 -*-
################################################################################
# !Disclaimer!
# Do not depend on this class if you aren't implementing anything in this
# library's internals. This class is considered a private class. There is no
# guarantee this class will function the same, or even exist at any point in the
# future.
################################################################################

import re


class TokenType:
    """
    This class acts as a type of enum, its possible types are:
        open_tag
        close_tag
        text
    """

    def __init__(self, _type):
        self._type = _type

    def __eq__(self, other: str):
        return self._type == other

    @classmethod
    def open_tag(cls):
        rv = cls('open_tag')

        return rv

    @classmethod
    def close_tag(cls):
        rv = cls('close_tag')

        return rv

    @classmethod
    def text(cls):
        rv = cls('text')

        return rv


class Token:
    def __init__(self, _type: TokenType, content: str):
        self.type = _type
        self.content = content

    def __repr__(self):
        return f'Token(type={self.type}, content={self.content})'


class Tokenizer:
    @staticmethod
    def tokenize(xml_string):
        tokens = []
        pattern = re.compile(r'<(/?)(\w+)(.*?)>')
        matches = pattern.finditer(xml_string)
        start = 0

        for match in matches:
            if match.start() > start:
                content = xml_string[start : match.start()]
                token = Token(TokenType.text(), content)
                tokens.append(token)

            content = match.group(0)
            if '/' in content:
                token = Token(TokenType.close_tag(), content)
            else:
                token = Token(TokenType.open_tag(), content)
            tokens.append(token)
            start = match.end()

        if start < len(xml_string):
            content = xml_string[start:]
            token = Token(TokenType.text(), content)
            tokens.append(token)

        return tokens
