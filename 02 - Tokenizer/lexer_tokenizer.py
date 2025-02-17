from lexer import *

# Keywords and Data Types
KEYWORD_MAIN = 'Main Function'
KEYWORD_RETURN = 'Return Statement'
DTYPE_INTEGER = 'Integer Data Type'

# Operators
OP_ASSIGN = 'Assignment Operator'
OP_ADDITION = 'Addition Operator'

# Delimiters
DELIM_SEMICOLON = 'Statement Terminator'
DELIM_COMMA = 'Comma Separator'

# Grouping Symbols
PAREN_OPEN = 'Opening Parenthesis'
PAREN_CLOSE = 'Closing Parenthesis'
BRACE_OPEN = 'Opening Curly Brace'
BRACE_CLOSE = 'Closing Curly Brace'

# Functions
FUNC_PRINT = 'Print Function'

# Literals
LITERAL_INTEGER = 'Integer Literal'
LITERAL_STRING = 'String Literal'
LITERAL_CHAR = 'Character Literal'

# Identifier
IDENTIFIER = 'Identifier'

# A function to make sure that a pattern matches as a whole word—preventing it from being part of larger words
def bound(pattern):
    return rf'(?<!\w){pattern}(?!\w)'

# Token expressions
TOKEN_PATTERNS = [
    (r'[ \n\t]+', None),  # Ignore whitespace(s)
    (bound('main'), KEYWORD_MAIN),
    (bound('return'), KEYWORD_RETURN),
    (bound('printf'), FUNC_PRINT),
    (bound('int'), DTYPE_INTEGER),
    (bound('='), OP_ASSIGN),
    (r'\+', OP_ADDITION),
    (r';', DELIM_SEMICOLON),
    (r',', DELIM_COMMA),
    (r'\(', PAREN_OPEN),
    (r'\)', PAREN_CLOSE),
    (r'\{', BRACE_OPEN),
    (r'\}', BRACE_CLOSE),
    (r'-?[0-9]+', LITERAL_INTEGER), 
    # (r'"[^"]*"', LITERAL_STRING),
    (r'"([^"\\]|\\.)*"', LITERAL_STRING),   # Also allow escaped quotes inside strings
    (r"'([^'\\]|\\.)'", LITERAL_CHAR),    # Chars 
    (r'[a-zA-Z_][a-zA-Z0-9_]*', IDENTIFIER),
]


def tokenize(characters):
    return lex(characters, TOKEN_PATTERNS)
