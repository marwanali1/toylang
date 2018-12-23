from lexer import Lexer
from parser import Parser
from code_gen import CodeGen

filename = 'input.toy'
with open(filename) as input_file:
    text_input = input_file.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

code_gen = CodeGen()
module = code_gen.module
builder = code_gen.builder
printf = code_gen.printf

parser_gen = Parser(module, builder, printf)
parser_gen.parse()
parser = parser_gen.get_parser()
parser.parse(tokens).eval()

code_gen.create_ir()
code_gen.save_ir('output.ll')
