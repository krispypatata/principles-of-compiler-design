# CMSC 129 - Week 05: YACC

## Author  
**Keith Ginoel S. Gabinete**  
*BS Computer Science*  
*CD-1L*  

## Program Description  
This is a simple program that checks the syntax and semantics of basic mathematical operations and string printing using lex and yacc, following Python rules.

## Prerequisites  
- bison 3.8.2
- flex 2.6.4 

## Usage  
To compile and run the program, execute the following commands one after another:  

```sh  
yacc -d GABINETEKG_exer5.y
lex GABINETEKG_exer5.l
cc y.tab.c lex.yy.c -o GABINETEKG_exer5.exe 
```  

OR, to compile and run everything at once (using the given Makefile), use:  

```sh  
make run  
```
or simply:
```sh  
make
```

To remove/clean generated files, use:  

```sh  
make clean  
```

## Notes  
- Basic operations supported include addition, subtraction, multiplication, division, and simple printing of strings.  

- Use `print()` to **print** a string:  
  - Strings must be enclosed in either **double** or **single** quotes.  
  - If a string is enclosed in **double** quotes, it **can contain** **single** quotes.  
  - If a string is enclosed in **single** quotes, it **can contain** **double** quotes.  
  - Only **one** string parameter is supported at a time.  

- To **terminate** the program, just type `exit()`.  
