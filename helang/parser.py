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
        root_parsers = [self._root_parse_u8_set, self._root_parse_var_def, self._root_parse_expr]
        asts = []
        while self._pos < len(self._tokens):
            for parser in root_parsers:
                saved_pos = self._pos
                try:
                    asts.append(parser())
                    break
                except BadStatementException:
                    self._pos = saved_pos
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

    def _root_parse_u8_set(self) -> U8SetAST:
        list_expr, subscript_expr = self._parse_u8_common_parts()
        self._get_token(0, TokenKind.RS)
        self._get_token(1, TokenKind.ASSIGN)
        self._pos += 2
        value_expr = self._root_parse_expr()
        return U8SetAST(list_expr, subscript_expr, value_expr)

    def _root_parse_expr(self, skip_u8=False) -> AST:
        expr_parsers = [self._parse_empty_u8_expr, self._parse_or_u8_expr, self._parse_u8_get, self._parse_var_expr]
        for parser in expr_parsers:
            if skip_u8 and parser == self._parse_u8_get:
                continue
            saved_pos = self._pos
            try:
                return parser()
            except BadStatementException:
                self._pos = saved_pos
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

    def _parse_var_expr(self) -> VarExprAST:
        ident = self._get_token(0, TokenKind.IDENT)
        self._pos += 1
        return VarExprAST(ident.content)

    def _parse_u8_get(self) -> U8GetAST:
        list_expr, subscript_expr = self._parse_u8_common_parts()
        self._get_token(0, TokenKind.RS)
        self._pos += 1
        return U8GetAST(list_expr, subscript_expr)

    def _parse_u8_common_parts(self) -> Tuple[AST, AST]:
        list_expr = self._root_parse_expr(skip_u8=True)
        self._get_token(0, TokenKind.LS)
        self._pos += 1
        subscript_expr = self._root_parse_expr()
        return list_expr, subscript_expr
