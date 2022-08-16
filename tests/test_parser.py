import unittest

from helang.parser import Parser
from helang.lexer import Lexer


class ParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.code = """
            u8 list1 = 1 | 2 | 3
            u8 list2 = [3]
        """

    def test_parse(self):
        lexer = Lexer(self.code)
        env = dict()
        Parser(lexer.lex()).parse().evaluate(env)
        self.assertEqual(env['list1'].value, [1, 2, 3])
        self.assertEqual(env['list2'].value, [0, 0, 0])
