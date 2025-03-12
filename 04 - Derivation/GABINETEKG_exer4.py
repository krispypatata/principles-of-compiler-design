# Gabinete, Keith Ginoel S.
# March 12, 2025
# CMSC 129 - CD-1L

import sys # Will only be used for debugging (using sys.exit() anywhere in the code)
TOLERANCE_MULTIPLIER = 5 # For setting limits in BFS (to avoid infinite loop or waiting for a long period of time)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function to read inputs from a file until EOF
# Returns a list of productions and strings to derive
def readInput():
    productions = []
    stringsToDerive = []

    # Flags for categorizing inputs
    readingProductions = False
    readingStringsToDerive = False

    try:
        while True:
            line = input().strip()      # Remove leading and trailing whitespace(s)

            formattedLine = ' '.join(line.split()) # Remove extra spaces between words

            # Categorize inputs into productions or strings to derived
            if formattedLine.lower() == "productions":
                readingProductions = True
                readingStringsToDerive = False
                continue

            if formattedLine.lower() == "strings to derive":
                readingStringsToDerive = True
                readingProductions = False
                continue

            if readingProductions: productions.append(line)

            if readingStringsToDerive: stringsToDerive.append(line)

    except EOFError:
        pass  # End of input file reached

    return productions, stringsToDerive

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function to create a context-free grammar using the productions list
def parseProductions(productions):
    grammar = {}
    for production in productions:
        # Extract the left and right hand sides
        leftHand, rightHand = production.split("->")
        leftHand = leftHand.strip()

        # Extract the rules from the right hand side
        unformattedRules = rightHand.split("|")
        rules = []
        for unformattedRule in unformattedRules:
            rule = unformattedRule.strip()
            rules.append(rule)

        # Store the nonterminal symbol and its rules in the dictionary
        grammar[leftHand] = rules

    return grammar

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function to get the steps in deriving the input string from a given set of production rules using leftmost derivation
def leftmostDerivation(grammar, startingSymbol, inputString):
    # Simple subfunction to remove unnecessary spaces and null/empty symbols from a given string input (Ex. input string to derive OR current derivation)
    # Will be used when comparing the current derivation with the input string we want to derive
    def normalize(derivedString):
        return ' '.join(derivedString.replace("#", "").split())

    # Use Breadth First Search to generate derivations of cfg
    queue = [(startingSymbol, [startingSymbol])]
    visited = set()

    targetString = normalize(inputString)

    while queue:
        # Generate next derivation
        currentDerivation, steps = queue.pop(0)
        normalizedDerivation = normalize(currentDerivation)

        # Successfully derived the input string
        if normalizedDerivation == targetString:
            return steps

        # Fix looping indefinitely by assuming that derivation is not possible given the length of the current derivation
        # Cause we can only tolerate a finite number of '#' symbols in the derivation as well
        # I just set the length limit to TOLERANCE_MULTIPLIERx of the input string cause I think that's already a generous amount
        if len(currentDerivation) > len(targetString) * TOLERANCE_MULTIPLIER: break

        # Perform leftmost derivation by replacing the leftmost nonterminal symbol
        for i in range(len(currentDerivation)):
            symbol = currentDerivation[i]

            # Check if the symbol is a nonterminal symbol (that is present in the grammar)
            if symbol in grammar:
                for rule in grammar[symbol]:
                    # Replace the nonterminal symbol with the current production rule
                    newDerivation = currentDerivation[:i] + rule + currentDerivation[i+1:]

                     # Avoid revisiting the same derivation
                    if newDerivation not in visited:
                        visited.add(newDerivation)
                        queue.append((newDerivation, steps + [newDerivation]))

                break # To ensure that only the leftmost nonterminal is replaced at each step

    return [  
        f"No valid derivation found!\n"  
    ]


# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Start of the main program
def main():
    # Read inputs
    # Usage:
    # [program] = this program's file name (Ex. 'GABINETE_exer4.py')
    # [input] = the input file to feed in the program (Ex. 'input.txt')
    # In the terminal type the following:
    # python3 [program] < [input]

    # Extract the production rules and the string(s) to derive
    productions, stringsToDerive = readInput()
    # print(productions, stringsToDerive)

    # Create the context-free grammar
    grammar = parseProductions(productions)
    # print(grammar)
    
    # Extract the starting symbol (This program always assume that the starting symbol is in the first line of productions in the input file)
    startSymbol = productions[0].split("->")[0].strip()

    # Some message to user(s) about the program
    print(
        f"[NOTE:] If no valid derivation is found, either the input string cannot be derived from the given grammar, or the length of the current derivation has exceeded the limit that this program can generate, which is {TOLERANCE_MULTIPLIER} times the length of the input string.\n\n"
        f"[SUGGESTION: You may also try adjusting the limit 'TOLERANCE_MULTIPLIER' in the code to allow longer derivations if you are certain that your input can be derived using the given set of production rules. However, if that doesn't work, the input might simply be too long for this program to process. It may take a long time, so you may choose to wait or terminate the program since the author is also unsure if the implementation is optimal due to using BFS to generate derivations.]\n"
    )

    print("══════════════════════════════════════════════") # Some divider

    # Perform leftmost derivation on the cfg to arrive at the given input string(s)
    for index, stringToDerive in enumerate(stringsToDerive):
        steps = leftmostDerivation(grammar, startSymbol, stringToDerive)

        print("String to derive:", stringToDerive)

        print("\nLeftmost derivation:")
        for iStep, step in enumerate(steps):
            # Arrow for each step besides the first step (starting symbol)
            if iStep > 0:
                print("->", end=" ")
            print(step)

        # Print new line between each iteration
        if index < len(stringsToDerive) - 1: print()

        

if __name__ == "__main__":
    main()
