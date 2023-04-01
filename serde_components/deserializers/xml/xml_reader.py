# -*- coding: utf-8 -*-
################################################################################
# !Disclaimer!
# Do not depend on this class if you aren't implementing anything in this
# library's internals. This class is considered a private class. There is no
# guarantee this class will function the same, or even exist at any point in the
# future.
################################################################################


from typing import List

from .tokenizer import Tokenizer


class XmlReader:
    """
    This class will act as a library. For this reason there is no internal state.
    """

    @staticmethod
    def loads(data: str) -> str:
        tokens = Tokenizer.tokenize(data)
        chain: List[str] = []
        depth = 0
        for token in tokens:
            if token.type == 'open_tag':
                depth += 1
                chain.append(token.content)
            elif token.type == 'close_tag':
                if chain and chain[-1] == token.content.replace('/', ''):
                    depth -= 1
                    chain.pop()
            else:
                # Its text
                pass
