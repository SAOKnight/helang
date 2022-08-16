from helang.lexer import Lexer
from helang.parser import Parser


if __name__ == '__main__':
    with open('../great.he', 'r') as f:
        content = f.read()
    lexer = Lexer(content)
    parser = Parser(lexer.lex())
    env = dict()
    parser.parse().evaluate(env)
