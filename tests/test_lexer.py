import unittest

from helang.lexer import Lexer
from helang.tokens import Token, TokenKind


class LexerTester(unittest.TestCase):
    def setUp(self) -> None:
        self.code = """
            for (u8 i = 0; i < 68; i++) {}
        """

    def test_lex(self):
        lexer = Lexer(self.code)
        tokens = lexer.lex()

        expected = [
            Token('for', TokenKind.KEYWORD),
            Token('(', TokenKind.LP),
            Token('u8', TokenKind.TYPE),
            Token('i', TokenKind.IDENT),
            Token('=', TokenKind.ASSIGN),
            Token('0', TokenKind.NUMBER),
            Token(';', TokenKind.SEMICOLON),
            Token('i', TokenKind.IDENT),
            Token('<', TokenKind.LT),
            Token('68', TokenKind.NUMBER),
            Token(';', TokenKind.SEMICOLON),
            Token('i', TokenKind.IDENT),
            Token('++', TokenKind.INCREMENT),
            Token(')', TokenKind.RP),
            Token('{', TokenKind.LC),
            Token('}', TokenKind.RC)
        ]

        for i in range(len(expected)):
            self.assertEqual(tokens[i], expected[i])
