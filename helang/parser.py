from helang.tokens import Token, TokenKind
from helang.exceptions import BadStatementException
from helang.he_ast import *
from typing import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._pos = 0

    def _get_token(self, offset: int, expected_kind: TokenKind, validator: Optional[Callable[[Token], bool]] = None):
        index = self._pos + offset

        if index >= len(self._tokens):
            raise BadStatementException('no more tokens')

        token = self._tokens[index]

        if token.kind != expected_kind:
            raise BadStatementException(f'expected {expected_kind} at offset {offset}, got {token.kind}')

        if validator is not None and not validator(token):
            raise BadStatementException(f'failed to pass custom validator at offset {offset}')

        return token

    def parse(self) -> AST:
        root_parsers = [self._root_parse_expr, self._root_parse_var_def]
        asts = []
        while self._pos < len(self._tokens):
            for parser in root_parsers:
                try:
                    asts.append(parser())
                    break
                except BadStatementException:
                    ...
            else:
                raise BadStatementException(f'failed to parse tokens started from {self._pos}')
        return ListAST(asts)

    def _root_parse_var_def(self) -> AST:
        self._get_token(0, TokenKind.U8)
        var_ident = self._get_token(1, TokenKind.IDENT)
        self._get_token(2, TokenKind.ASSIGN)
        self._pos += 3
        val = self._root_parse_expr()
        return VarDefAST(var_ident.content, val)

    def _root_parse_expr(self) -> AST:
        expr_parsers = [self._parse_empty_u8_expr, self._parse_or_u8_expr]
        for parser in expr_parsers:
            try:
                return parser()
            except BadStatementException:
                ...
        raise BadStatementException('cannot parse expressions')

    def _parse_empty_u8_expr(self) -> AST:
        self._get_token(0, TokenKind.LS)
        length = self._get_token(1, TokenKind.NUMBER)
        self._get_token(2, TokenKind.RS)
        self._pos += 3
        return EmptyU8InitAST(int(length.content))

    def _parse_or_u8_expr(self) -> OrU8InitAST:
        first = self._get_token(0, TokenKind.NUMBER)

        try:
            self._get_token(1, TokenKind.OR)
        except BadStatementException:
            # Skip current number.
            self._pos += 1
            return OrU8InitAST(int(first.content))

        self._pos += 2
        return OrU8InitAST(int(first.content), self._parse_or_u8_expr())
