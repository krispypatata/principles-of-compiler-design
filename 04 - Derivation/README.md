# CMSC 129 - Week 04: Derivation

## Author  
**Keith Ginoel S. Gabinete**  
*BS Computer Science*  
*CD-1L*  

## Program Description  
This is a simple Python program that attempts to derive a given input string from a set of production rules using leftmost derivation. The steps of the derivation process are displayed in the terminal.   

## Prerequisites  
- Python 3.x must be installed.  

## Usage  
To run the program, use one of the following commands:  

```sh  
python3 GABINETEKG_exer4.py < input.txt  
```  

OR (Using the given Makefile)  

```sh  
make  
```  

## Testing with Custom Inputs  
To test different inputs, modify `input.txt` as follows:  
1. Under **Productions**, list the production rules that define the Context-Free Grammar.  
2. Under **Strings to derive**, specify the strings to derive using the production rules.  

**IMPORTANT!**:  
- Use `#` to represent `ε` (the empty or null symbol).  
- The **left-hand side** of the **first** production rule is considered the **starting symbol**.  
- Do not delete the strings **"Productions"** and **"Strings to derive"** in `input.txt`; otherwise, the program will not function correctly.  
- Use **UPPERCASE letters** for nonterminal symbols and **lowercase letters** for terminal symbols. 

### Example of a valid input file:
```
Productions  
A -> C B  
B -> + C B | #  
C -> E D  
D -> * E D | #  
E -> ( A ) | n  
Strings to derive  
n + n * n  
```

## Output  
The program displays the step-by-step leftmost derivation of the input string in the terminal.  

### Sample Output:
```
A  
-> C B  
-> E D B  
-> n D B  
-> n # B  
-> n # + C B  
-> n # + E D B  
-> n # + n D B  
-> n # + n * E D B  
-> n # + n * n D B  
-> n # + n * n # B  
-> n # + n * n # #  
```

## Notes  
If no valid derivation is found, it may be due to one of the following reasons:
- The input string cannot be derived from the given grammar.
- The derivation length exceeds the program’s processing limit, which is `TOLERANCE_MULTIPLIER` (default: 5) times the input string’s length.

If you are certain that your input can be derived using the given set of production rules:
- You may try adjusting the limit `TOLERANCE_MULTIPLIER` in the source code to allow longer derivations. However, if that doesn't work, the input might simply be too long for this program to process. It may take a long time, so you may choose to wait or terminate the program since the author is also unsure if the implementation is optimal due to using BFS to generate derivations.

