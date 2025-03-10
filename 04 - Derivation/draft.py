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




############################################################
# Sample
# S = grammars[0].split("|")
grammarRules = readLines[:-1]
stringToDerive = readLines[-1]


print(grammarRules)

# Extract rules
grammar = {}

for productions in grammarRules:
    leftHand, rightHand = productions.split("->")
    leftHand = leftHand.strip()

    unformattedRules = rightHand.split("|")
    rules = []
    for unformattedRule in unformattedRules:
        rule = unformattedRule.split()
        rules.append("".join(rule))

    grammar[leftHand] = rules

print(grammar)

############################################################
# grammar = {
#     "S": ["SS+", "SS*", "a"]
# }
stringToDerive = "aa+a*"

terminals = {"a" : "S"}

print(grammar["S"])


############################################################
# RIGHTMOST DERIVATION
steps = ["S"]
currentDerivation = steps[-1]

# print(steps)
# print(stringToDerive)
indexOfStringToDerive = len(stringToDerive) - 1
while (indexOfStringToDerive >= 0):
    currentChar = stringToDerive[indexOfStringToDerive]

    substringToReplace = ""
    for rule in grammar["S"]:
        if currentChar in rule:
            substringToReplace = rule
            break

    newDerivation = currentDerivation[::-1]
    newDerivation = newDerivation.replace("S", substringToReplace[::-1], 1)
    currentDerivation = newDerivation[::-1]
    steps.append(currentDerivation)
    indexOfStringToDerive -= 1

for s in steps:
    print(s)