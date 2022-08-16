import enum

from helang.tokens import Token
from helang.exceptions import BadStatementException
from typing import *


class ParserState(enum.Enum):
    ASSIGNMENT = 1


class Parser:
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens

    def parse(self):
        pass


