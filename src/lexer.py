from rply import LexerGenerator


class Lexer:
    """
    Takes the program as input and divides it into Tokens.
    """

    def __init__(self):
        self.lexer = LexerGenerator()

    def __add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')

        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        # Semi colon
        self.lexer.add('SEMI_COLON', r'\;')

        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')

        # Number
        self.lexer.add('NUMBER', r'\d+')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self.__add_tokens()
        return self.lexer.build()
