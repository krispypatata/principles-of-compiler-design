# Author: Gabinete, Keith Ginoel S.
# Date: February 17, 2025

import sys
import re

# ════════════════════════════════════════════════════════════════════════════════════════════════════════════
# LEXER
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# Function for tokenizing a string of characters based on a set of token patterns.
def lex(characters, token_exprs):
    pos = 0                 # Current position in the input string
    tokens = []             # List to hold the tokenized output
    line_number = 1         # Start with line number 1
    column_number = 1       
    last_newline_pos = -1   # Position of the last newline

    # Traverse through the contents of the input
    while pos < len(characters):
        match = None # Flag to track whether a match is found for the current position

        # traverse through the list of regex patterns for tokens
        for token_expr in token_exprs:
            pattern, tag = token_expr               # Extract regex pattern and tag from token_expr; ex. ('HAI', 'Reserved')
            regex = re.compile(pattern)             # Compile the regex
            match = regex.match(characters, pos)    # Try to match the pattern at the current position
            
            # If there's a match, get the matched text
            if match:
                text = match.group(0)

                # But only add token to the list if it has a valid tag 
                if tag:
                    token = (text, tag)
                    tokens.append(token)

                # Update line count if a newline is encountered in the matched text
                newline_count = text.count("\n")
                if newline_count > 0:
                    line_number += newline_count
                    last_newline_pos = pos + text.rfind("\n")  # Find the position of the last newline in the matched text (to be used in resetting column number)
                    column_number = pos - last_newline_pos
                else:
                    column_number += len(text)

                # Move the position to the end of the matched token
                pos = match.end(0)

                 # Exit the loop once a match is found
                break

        # If there's no match found, then there's an error
        if not match:
            column_number = pos - last_newline_pos  # Update column number with its correct position
            sys.stderr.write(f"Illegal character '{characters[pos]}' at line {line_number}, column {column_number}\n")
            sys.exit(1)
        
        # If match found, move the position pointer to the end of the matched text
        else:
            pos = match.end(0)
    
    # Return the list of tokens
    return tokens


# ════════════════════════════════════════════════════════════════════════════════════════════════════════════
# TOKENIZER
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# Keywords and Data Types
KEYWORD_MAIN = 'Main Function'
KEYWORD_RETURN = 'Return Statement'
TYPE_INTEGER = 'Integer Type'

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
    (bound('int'), TYPE_INTEGER),
    (bound('='), OP_ASSIGN),
    (r'\+', OP_ADDITION),
    (r';', DELIM_SEMICOLON),
    (r',', DELIM_COMMA),
    (r'\(', PAREN_OPEN),
    (r'\)', PAREN_CLOSE),
    (r'\{', BRACE_OPEN),
    (r'\}', BRACE_CLOSE),
    (r'-?[0-9]+', LITERAL_INTEGER), 
    (r'"([^"\\]|\\.)*"', LITERAL_STRING),   # Also allow escaped double quotes inside strings
    (r"'([^'\\]|\\.)'", LITERAL_CHAR),      # Also allow escaped single quotes inside characters
    (r'[a-zA-Z_][a-zA-Z0-9_]*', IDENTIFIER),
]


def tokenize(characters):
    return lex(characters, TOKEN_PATTERNS)


# ════════════════════════════════════════════════════════════════════════════════════════════════════════════
# HELPER/DRIVER
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# For testing the implementation of the lexer
if __name__ == '__main__':
    # Check for incorrect usage of the program
    if len(sys.argv) < 2:
        print("Usage: python GABINETE_exer2.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]
    # filename = 'sample1.txt'   # Override arguments; for testing

    characters = None
    try:
        file = open(filename, 'r')
        characters = file.read()
        file.close()  # Needed because 'with' is not used
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    print('INPUT:')
    print("-"*60)
    print(characters)
    print("-"*60)

    # For checking
    # print(characters)
    # print('\n\n\n\n\n')

    # Tokenize the characters read from the input file
    tokens = tokenize(characters)

    # For printing
    col1_width = 20  # token width
    col2_width = 30  # tag width
    col3_width = 10  # line number width

    # Header for printing
    HEADER = f'{"TOKEN".ljust(col1_width)}{"TAG".ljust(col2_width)}'
    HEADER_DIVIDER = "-" * (col1_width + col2_width + col3_width)

    # Print the tokens in an organized format
    print(HEADER)
    print(HEADER_DIVIDER)
    for token, tag in tokens:
        print(f'{token.ljust(col1_width)}{tag.ljust(col2_width)}')

    # Print the total number of tokens extracted
    print('')
    print(f'{"TOTAL:".ljust(col1_width)}{len(tokens)}')

    # output to a file (Optional)
    output_filename = "lexer.out"
    with open(output_filename, 'w') as output_file:
        # Write the header to the file
        output_file.write(HEADER + '\n')
        output_file.write(HEADER_DIVIDER + '\n')

        for token, tag in tokens:
            output_file.write(f'{token.ljust(col1_width)}{tag.ljust(col2_width)}' + '\n')

        output_file.write('\n')
        output_file.write(f'{"TOTAL:".ljust(col1_width)}{len(tokens)}' + '\n')
        
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════
