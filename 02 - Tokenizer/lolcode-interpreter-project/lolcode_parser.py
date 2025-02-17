from combinators import *
from lolcode_lexer import *
from functools import reduce
from lolcode_ast import *
import sys

# CONSTANTS
RESERVED = 'Reserved'
STRING = 'String'
INTEGER = 'Integer'
FLOAT = 'Float'
BOOLEAN = 'Boolean'
IDENTIFIER = 'Identifier'
NOOB = 'Noob'

# Basic parsers for different tokens
def keyword(kw):
    return Reserved(kw, RESERVED)  # Use the constant

# Parse different literal types
int_num = Tag(INTEGER) ^ (lambda i: int(i))  # Return the integer value directly
float_num = Tag(FLOAT) ^ (lambda f: float(f))  # Return the float value directly
string_literal = Tag(STRING) ^ (lambda s: s)  # Dtring literals
boolean_literal = Tag(BOOLEAN) ^ (lambda b: True if b == "WIN" else False)  # Return boolean directly
variable_identifier = Tag(IDENTIFIER)

# PRIMITIVES
def literal():
    return (
        int_num ^ (lambda parsed: Integer(parsed)) | 
        float_num ^ (lambda parsed: Float(parsed)) | 
        string_literal ^ (lambda parsed: String(parsed)) | 
        boolean_literal ^ (lambda parsed: Boolean(parsed))
    )
# literal = int_num | float_num | string_literal | boolean_literal
def identifier():
    return variable_identifier ^ (lambda parsed: Identifier(parsed))



# Top-level parser for the program
def lolcode_parse(tokens):
    ast = program()(tokens, 0)
    return ast

def program():
    parsed_program = Phrase(body())
    return parsed_program

def body():
    return keyword("HAI") + Opt(variable_declaration_section()) + statement_list() + keyword("KTHXBYE") ^ (lambda parsed: Program(parsed[0][0][1], parsed[0][1])) \
    | Error("Syntax error")
    # | Error("Expected 'HAI' followed by statements and 'KTHXBYE'")
    

# Variable declaration and initialization parsers
def variable_declaration_section():
    return keyword("WAZZUP") + Rep(variable_declaration()) + keyword("BUHBYE") ^ (lambda parsed: VariableSection(declarations=parsed[0][1])) | Error("Syntax error")
    #| Error("Expected 'WAZZUP' followed by variable declarations and 'BUHBYE'")

def variable_declaration():
    parsed_section = (
        (
        keyword("I HAS A") 
        + identifier()
        + Opt(
            keyword("ITZ") 
            + (literal() | identifier())
            )
        ) 
    
         # process
        ^ (lambda parsed: VariableDeclaration( name=parsed[0][1], initial_value=parsed[1][1] if parsed[1] is not None else None))
    )

    return parsed_section

# Parse multiple statements
def statement_list():
    return Rep(statement())  # This will repeat the statement parser

# Statement parsers
def statement():
    # Parse the VISIBLE statement followed by a literal
    return print_statement() | if_statement()

def print_statement():
    return (keyword("VISIBLE") + (identifier() | literal() | aexp() | bexp())) ^ (lambda parsed: PrintStatement(expression = parsed[1]))


def arithmetic_operation():
    return (
        ((keyword("SUM OF") | keyword("DIFF OF") | keyword("PRODUKT OF") | keyword("QUOSHUNT OF") | keyword("MOD OF") | keyword("BIGGR OF") | keyword("SMALLR OF")) 
        + basic_aexp() + keyword("AN") + basic_aexp()) ^ (lambda parsed: BinaryOperationAE(parsed[0][0][0], parsed[0][0][1], parsed[1])) 
    )

# Arithmetic expressions
def aexp():
    return (arithmetic_operation() | basic_aexp() )


def basic_aexp():
    return literal() | identifier()

# Boolean operations
def boolean_operation():
    return (
        (keyword("BOTH OF") + basic_aexp() + keyword("AN") + basic_aexp()) ^ (lambda parsed: BooleanBinaryOperationAE(parsed[0][0][0], parsed[0][0][1], parsed[1])) | 
        (keyword("EITHER OF") + basic_aexp() + keyword("AN") + basic_aexp()) ^ (lambda parsed: BooleanBinaryOperationAE(parsed[0][0][0], parsed[0][0][1], parsed[1])) | 
        (keyword("WON OF") + basic_aexp() + keyword("AN") + basic_aexp()) ^ (lambda parsed: BooleanBinaryOperationAE(parsed[0][0][0], parsed[0][0][1], parsed[1])) | 
        (keyword("NOT") + basic_aexp()) ^ (lambda parsed: BooleanBinaryOperationAE(parsed[0], parsed[1])) | 
        (keyword("ALL OF") + Rep(basic_aexp() + keyword("AN")) + basic_aexp() + keyword("MKAY")) ^ (lambda parsed: f"({' and '.join(map(str, parsed[0][0][1]))})") | 
        (keyword("ANY OF") + Rep(basic_aexp() + keyword("AN")) + basic_aexp() + keyword("MKAY")) ^ (lambda parsed: f"({' or '.join(map(str, parsed[0][0][1]))})")
    )

def bexp():
    return boolean_operation() | comparison_operation() | literal() | identifier()

# Comparison operations
def comparison_operation():
    return (keyword("BOTH SAEM") + aexp() + keyword("AN") + aexp()) ^ (lambda parsed: f"({parsed[1]} == {parsed[3]})") | \
           (keyword("DIFFRINT") + aexp() + keyword("AN") + aexp()) ^ (lambda parsed: f"({parsed[1]} != {parsed[3]})")

def if_statement():
    def process(parsed):
        print(parsed)
        (((((condition, _), _), true_stmt), false_parsed), _) = parsed

        print(condition)
        print(true_stmt)
        print(false_parsed)
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        
        return IfStatement(condition, true_stmt, false_stmt)
        # return IfStatement(0, 1, 2)
    
    # return boolean_operation() ^ process
    return (
        boolean_operation() +
        keyword('O RLY?') +
        keyword('YA RLY') + print_statement() + 
        Opt(keyword('NO WAI') + print_statement() ) + 
        keyword('OIC') 
    ) ^ process


# Function for printing the symbol table
def symtab(env):
    header = "| {:<10} | {:<10} |".format("Variable", "Value")
    separator = "+" + "-"*12 + "+" + "-"*12 + "+"  # border
    print(separator)
    print(header)
    print(separator)

    for name, value in env.items():
        value_str = str(value) if value is not None else "None"  # handle None values
        print("| {:<10} | {:<10} |".format(name, value_str))
    
    print(separator)

# Function for displaying symbol table in gui
def generate_symtab(tokens):
    parse_result = lolcode_parse(tokens)
    ast = parse_result.value

    env = {}
    ast.eval(env)

    return env

# Test code
if __name__ == "__main__":
    code1 = """
    HAI
    WAZZUP
    I HAS A thing1
    I HAS A thing2 ITZ "some"
    I HAS A thing3 ITZ 3.14
    BUHBYE
    VISIBLE "HELLO WORLD"
    VISIBLE 1.2
    VISIBLE 3.14
    VISIBLE thing1
    VISIBLE thing2
    VISIBLE thing3
    VISIBLE WIN
    VISIBLE FAIL
    VISIBLE SUM OF 2 AN 4
    VISIBLE DIFF OF 4 AN -3
    VISIBLE PRODUKT OF 2 AN 7
    VISIBLE QUOSHUNT OF 5 AN 12
    VISIBLE MOD OF 3.2 AN 3.14
    VISIBLE BIGGR OF 3.2 AN 3.14
    VISIBLE SMALLR OF 3.2 AN 3.14
    VISIBLE BOTH OF WIN AN FAIL
    VISIBLE EITHER OF WIN AN FAIL
    VISIBLE WON OF WIN AN FAIL
    VISIBLE NOT WIN
    NOT WIN
    O RLY?
        YA RLY
            VISIBLE "TRUE STATEMENT"
        NO WAI
            VISIBLE "FALSE STATEMENT"
    OIC
    KTHXBYE
    """

    code2 = """
    HAI
    WAZZUP
    I HAS A thing
    I HAS A thing2 ITZ "some"
    I HAS A thing3 ITZ 3.14
    BUHBYE
    VISIBLE "HELLO WORLD"
    VISIBLE 1.2
    VISIBLE 3.14
    VISIBLE WIN
    VISIBLE FAIL
    VISIBLE SUM OF 2 AN 4
    VISIBLE DIFF OF 4 AN 3
    VISIBLE PRODUKT OF 2 AN 7
    VISIBLE QUOSHUNT OF 5 AN 12
    VISIBLE MOD OF 3.2 AN 3.14
    VISIBLE BIGGR OF 3.2 AN 3.14
    VISIBLE SMALLR OF 3.2 AN 3.14
    VISIBLE BOTH OF WIN AN FAIL
    VISIBLE EITHER OF WIN AN FAIL
    VISIBLE WON OF WIN AN FAIL
    VISIBLE NOT WIN
    KTHXBYE
    """
    tokens = lolcode_lex(code2)
    print("Tokens:", tokens)  # Debug: Check token output
    
    # REPLACE WITH 'KEYWORD'
    for i in range(len(tokens)):
        token = tokens[i]

        if token[1] not in (STRING, INTEGER, FLOAT, BOOLEAN, IDENTIFIER, NOOB, LITERAL_TYPE):
            token_update = (token[0], 'Reserved', token[1])
            tokens[i] = token_update

    try:
        parse_result = lolcode_parse(tokens)
        ast = parse_result.value
        print("\nAST:\n", ast)  # Should display the parsed AST with HAI, WAZZUP, and KTXHBYE

        # Execute the program
        print("\nExecution:")
        env = {}  # Initialize an environment
        ast.eval(env)

        sys.stdout.write('\nFinal variable values:\n')
        for name in env:
            sys.stdout.write('%s: %s\n' % (name, env[name]))
        
        print("\nTable Format:")
        symtab(env)
    except SyntaxError as e:
        print(f"\nParsing failed: {e}")

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]