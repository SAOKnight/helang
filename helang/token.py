import enum


class TokenKind(enum.Enum):
    # Numbers like 123, 276, etc.
    NUMBER = 1
    # |
    OR = 2
    # Types like u8, void
    TYPE = 3
    # Identifiers
    IDENT = 4
    # (
    LP = 5
    # )
    RP = 6
    # {
    LC = 7
    # }
    RC = 8
    # [
    LS = 9
    # ]
    RS = 10
    # ,
    COMMA = 11
    # ;
    SEMICOLON = 12
    # -
    MINUS = 13
    # =
    ASSIGN = 14
    # Less than, <
    LT = 15
    # Keyword if
    IF = 16
    # Keyword for
    FOR = 17


class Token:
    def __init__(self, content: str, kind: TokenKind):
        self.content = content
        self.kind = kind
