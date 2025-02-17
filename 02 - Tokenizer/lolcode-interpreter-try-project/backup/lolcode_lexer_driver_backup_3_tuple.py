import sys
from lolcode_lexer import *
from multi_line_comment_validator import validate_multiline_comments

# For testing the implementation of the lexer
if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    validate_multiline_comments(characters) # Validate the existence of multi-line comments
    tokens = lolcode_lex(characters)

    # For printing
    col1_width = 20  # token width
    col2_width = 30  # tag width
    col3_width = 10  # line number width

    # Header for printing
    HEADER = f'{"TOKEN".ljust(col1_width)}{"TAG".ljust(col2_width)}{"LINE_NUMBER".ljust(col3_width)}'
    HEADER_DIVIDER = "-" * (col1_width + col2_width + col3_width)

    # Print the tokens in an organized format
    print(HEADER)
    print(HEADER_DIVIDER)
    for token, tag, line_number in tokens:
        print(f'{token.ljust(col1_width)}{tag.ljust(col2_width)}{str(line_number).ljust(col3_width)}')


    # output to a file
    output_filename = "output.txt"
    with open(output_filename, 'w') as output_file:
        # Write the header to the file
        output_file.write(HEADER + '\n')
        output_file.write(HEADER_DIVIDER + '\n')

        for token, tag, line_number in tokens:
            output_file.write(f'{token.ljust(col1_width)}{tag.ljust(col2_width)}{str(line_number).ljust(col3_width)}' + '\n')
        