%{
	/*
	Gabinete, Keith Ginoel S.
	March 31, 2025
	CMSC 129 - CD-1L
	*/

	#include <stdio.h>
	#include <stdlib.h>

	int regs[26];
	int base;

	int yywrap();
	extern int yylex();
	int yyerror(const char *s);

	void display_prompt(void);
%}

/* A union to store integers and strings */
%union {
    int num;
    char *str;
}

/* Token declarations with associated data types */
%start list
%token <num> DIGIT LETTER
%token <str> PRINT
%token QUIT

/* Define data type of non-terminal symbols*/
%type <num> expr stat number

/* Operator precedence and associativity rules */
%left '|'
%left '&'
%left '+' '-'
%left '*' '/' '%'
%left UMINUS /*supplies precedence for unary minus */

%% /* beginning of rules section */
list : /*empty */
    | list PRINT '\n'
	{
        printf("%s\n", $2);
        free($2);

		display_prompt();
    }

    | list QUIT 
	{	/* Exit the program */
		printf("Exiting program... Goodbye!\n");
		exit(0);
	}

	| list stat '\n' 
	{ display_prompt(); }

	| list error '\n'
	{ yyerrok; /* used to stop discarding tokens */ display_prompt(); }
	; /* End of list */

stat : expr
	{ printf("%d\n",$1); }

	| LETTER '=' expr
	{ regs[$1] = $3; }
	; /* End of stat */


expr : '(' expr ')' 
	{ $$ = $2; }
	
	| expr '*' expr 
	{ $$ = $1 * $3; }

	| expr '/' expr 
	{ $$ = $1 / $3; }
	
	| expr '%' expr 
	{ $$ = $1 % $3; }
	
	| expr '+' expr 
	{ $$ = $1 + $3; }
	
	| expr '-' expr
	{ $$ = $1 - $3; }
	
	| expr '&' expr 
	{ $$ = $1 & $3; }
	
	| expr '|' expr 
	{ $$ = $1 | $3; }
	
	| '-' expr %prec UMINUS 
	{ $$ = -$2; }
	
	| LETTER 
	{ $$ = regs[$1]; }
	
	| number
	; /* End of exp */

number : DIGIT 
	{
		$$ = $1;
		base = ($1==0) ? 8 : 10;
	}
	| number DIGIT 
	{
		$$ = base * $1 + $2;
	}
	; /* End of number */

%%
int yyerror (const char *s)
{
	fprintf(stderr, "%s\n",s);
}

int yywrap() {
	return(1);
}

void display_prompt(void) {
    printf(">>> ");
    fflush(stdout);
}

int main() {
	/* Some greeting message */
	printf(
		"═════════════════════════════════════════════════════════════════════════\n"
	);
	printf(
		"This is a simple program that checks the syntax and semantics of basic\n"
		"mathematical operations and string printing using lex and yacc, following\n"
		"Python rules.\n\n"
	);

	printf(
		"Basic operations supported include addition, subtraction, multiplication,\n"
		"division, and simple printing of strings.\n\n"
	);

	printf(
		"Use print() to print a string.\n"
		"Strings must be enclosed in either double or single quotes.\n"
		"If a string is enclosed in double quotes, it can contain single quotes.\n"
		"If a string is enclosed in single quotes, it can contain double quotes.\n"
		"Only one string parameter is supported at a time.\n\n"
	);

	printf(
		"To terminate the program, just type 'exit()'.\n"
	);

	printf(
		"═════════════════════════════════════════════════════════════════════════\n"
	);
	
	display_prompt();

	return(yyparse());
}
