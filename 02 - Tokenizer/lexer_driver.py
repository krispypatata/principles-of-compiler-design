import sys
from lexer_tokenizer import *
from lexer import *

# For testing the implementation of the lexer
if __name__ == '__main__':
    filename = sys.argv[1]
    # filename = 'sample1.txt'   # Override arguments
    file = open(filename)
    characters = file.read()
    file.close()

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
        