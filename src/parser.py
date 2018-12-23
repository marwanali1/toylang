from rply import ParserGenerator
from ast import Number, Add, Sub, Print


class Parser:
    """
    Does a syntax check of the program. It takes a list of tokens as input and
    creates an AST as output.
    """

    def __init__(self, module, builder, printf):
        # A list of all tokens accepted by the parser
        accepted_tokens = ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'SEMI_COLON', 'ADD', 'SUB']
        self.parser_gen = ParserGenerator(tokens=accepted_tokens)
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):

        @self.parser_gen.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def program(p):
            return Print(self.module, self.builder, self.printf, p[2])

        @self.parser_gen.production('expression : expression ADD expression')
        @self.parser_gen.production('expression : expression SUB expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]

            if operator.gettokentype() == 'ADD':
                return Add(self.module, self.builder, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.module, self.builder, left, right)

        @self.parser_gen.production('expression : NUMBER')
        def number(p):
            return Number(self.module, self.builder, p[0].value)

        @self.parser_gen.error
        def error_handler(token):
            raise ValueError(token)

    def get_parser(self):
        return self.parser_gen.build()
