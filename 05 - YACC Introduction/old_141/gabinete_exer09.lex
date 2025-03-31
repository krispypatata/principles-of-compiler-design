/*
  Gabinete, Keith Ginoel S.
  CMSC 141 - D1L
  Exercise No. 9 - Introduction to lex|flex and yacc|bison for language translators
*/
%{ // Section 1: declaration and option settings
  #include "gabinete_exer09.tab.h"
%}

INT	    [0-9]+
FLOAT   [0-9]*\.[0-9]+
VAR     [a-zA-Z]

%% // Section 2: rules
"+"			{return ADD;}
"-"			{return SUB;}
"/"			{return DIV;}
"*"			{return MUL;}
"!"     {return NEG;}   // unary minus
"^"     {return POW;}
"="     {return ASS;}
{INT}		{yylval = atoi(yytext); return INTEGER;}  // parse as float
{FLOAT}	{yylval = atof(yytext); return FLOAT;}    // parse as integer
{VAR}   {yylval = *yytext; return VAR_NAME;}      // one-letter variable name only
\n			{return EOL;}
[[:space:]]	{/*ignore white space*/}
"exit"		{return QUIT;}
.			{printf("\nUnrecognized string %c\n", *yytext);}
%%
