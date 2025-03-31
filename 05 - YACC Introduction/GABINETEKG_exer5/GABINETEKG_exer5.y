%{
	#include <stdio.h>
	int regs[26];
	int base;

	int yywrap();
	extern int yylex();
	int yyerror(const char *s);

    #define ECHO fwrite(yytext, yyleng, 1, yyout)
%}

%start list
%token DIGIT LETTER
%token PRINT
%token QUIT
%left '|'
%left '&'
%left '+' '-'
%left '*' '/' '%'
%left UMINUS /*supplies precedence for unary minus */

%% /* beginning of rules section */
list : /*empty */
    | list PRINT '\n'
    | list QUIT {printf("Exiting...\n"); return 0;}  // exit the program
	| list stat '\n'
	| list error '\n'
	{
		yyerrok; /* used to stop discarding tokens */
	}
	;

stat : expr
	{
		printf("%d\n",$1);
	}
	| LETTER '=' expr
	{
		regs[$1] = $3;
	}
	;


expr : '(' expr ')' 
	{
		$$ = $2;
	}
	
	| expr '*' expr 
	{
		$$ = $1 * $3;
	}

	| expr '/' expr 
	{
		$$ = $1 / $3;
	}
	
	| expr '%' expr 
	{
		$$ = $1 % $3;
	}
	
	| expr '+' expr 
	{
		$$ = $1 + $3;
	}
	
	| expr '-' expr
	{
		$$ = $1 - $3;
	}
	
	| expr '&' expr 
	{
		$$ = $1 & $3;
	}
	
	| expr '|' expr 
	{
		$$ = $1 | $3;
	}
	
	| '-' expr %prec UMINUS 
	{
		$$ = -$2;
	}
	
	| LETTER 
	{
		$$ = regs[$1];
	}
	
	| number
	;

number : DIGIT 
	{
		$$ = $1;
		base = ($1==0) ? 8 : 10;
	}
	| number DIGIT 
	{
		$$ = base * $1 + $2;
	}
	;

%%
int yyerror (const char *s)
{
	fprintf(stderr, "%s\n",s);
}

int yywrap() {
	return(1);
}

int main() {
	return(yyparse());
}