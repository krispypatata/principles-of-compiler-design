# Gabinete, Keith Ginoel S.
# March 10, 2025
# CMSC 129 - CD-1L

import sys

# if __name__ == "__main__":
#     readInputs = input().split()
#     print(readInputs)
#     derive(readInputs)
############################################################
readLines = []
while True:
    line = input()

    if line.strip() == "-1": break

    if line: readLines.append(line)

grammars = readLines[:-1]
stringToDerive = readLines[-1]
# print(grammars, "\n", stringToDerive)
# inputString = "".join(readInputSymbols)

############################################################
# Sample
# S = grammars[0].split("|")

S = ["SS+", "SS*", "a"]
stringToDerive = "aa+a*"

terminals = {"a" : "S"}

print(S)

sys.exit()

############################################################
currentDerivation = stringToDerive
steps = [stringToDerive]

index = len(currentDerivation) - 1
# Transform terminals into nonterminal symbols
while index >= 0:
    # print(currentDerivation[index])
    if currentDerivation[index] in terminals:
        currentDerivationAsList = list(currentDerivation)
        currentDerivationAsList[index] = terminals[currentDerivation[index]]
        currentDerivation = "".join(currentDerivationAsList)
        steps.append(currentDerivation)
    index -= 1

# Transform nonterminals
while True:
    if len(currentDerivation) <= 1: break

    hasStopped = False
    substringToTransform = ""
    indexOfCharToTransform = 0
    for i in range(len(currentDerivation) - 1, -1, -1):
        if hasStopped: break

        substringToTransform = ""
        for j in range(i, -1, -1):
            substringToTransform = currentDerivation[j] + substringToTransform

            if substringToTransform in S:
                indexOfCharToTransform = j
                hasStopped = True
                break

    # Replace 
    transformedDerivation = currentDerivation[::-1]
    transformedDerivation = transformedDerivation.replace(substringToTransform[::-1], "S", 1)
    currentDerivation = transformedDerivation[::-1]
    steps.append(currentDerivation)

# Print the derivation
# Testing
for s in steps[::-1]:
    print(s)