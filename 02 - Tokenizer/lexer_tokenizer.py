from lexer import *

# Proram keywords, variables
MAIN = 'Start of the Main program'
DATA_TYPE = "Data Type"
INTEGER = 'Integer'
STRING = 'String'
ASSIGNMENT = 'Assignment Operator'


SEMICOLON = 'Statement Delimeter'
COMMA = 'Statement Separator'

OPEN_PAREN = 'Open Parenthesis'
CLOSE_PAREN = 'Close Parenthesis'

OPEN_CURL = 'Open Curly Bracket'
CLOSE_CURL = 'Close Curly Bracket'
ADDITION = 'Addition Operator'

RETURN = 'Return Keyword'

# Statements
PRINTF = 'Print Function'

# Identifier
IDENTIFIER = 'Identifier'

# Make sure that the pattern matches as a whole word, excluding it from being part of larger words.
def bound(pattern):
    return rf'(?<!\w){pattern}(?!\w)'

token_exprs = [
    (r'[ \n\t]+', None),  # Ignore whitespace(s)
    (bound('main'), MAIN),
    (bound('='), ASSIGNMENT),
    (r'\+', ADDITION),
    (r';', SEMICOLON),
    (r',', COMMA),
    (r'\(', OPEN_PAREN),
    (r'\)', CLOSE_PAREN),
    (r'\{', OPEN_CURL),
    (r'\}', CLOSE_CURL),
    (bound('return'), RETURN),
    (bound('printf'), PRINTF),
    (r'-?[0-9]+', INTEGER), 
    (r'"[^"]*"', STRING),                    # String
    (bound('int'), DATA_TYPE),               # Data type
    (r'[a-zA-Z][a-zA-Z0-9_]*', IDENTIFIER),  # Identifier
]


def tokenize(characters):
    return lex(characters, token_exprs)
