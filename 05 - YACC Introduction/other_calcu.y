%{
#include <stdio.h>
int regs[26];
int base;

int yywrap();
extern int yylex();
int yyerror(const char *s);
%}
%start list
%token DIGIT LETTER
%left '|'
%left '&'
%left '+' '-'
%left '*' '/' '%'
%left UMINUS /*supplies precedence for unary minus */

%% /* beginning of rules section */
list : /*empty */
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

expr : '(' expr ')' {
$$ = $2;
}
| expr '*' expr {
$$ = $1 * $3;
}

| expr '/' expr {
$$ = $1 / $3;
}
| expr '%' expr {
$$ = $1 % $3;
}
| expr '+' expr {
$$ = $1 + $3;
}

| expr '
-' expr
{
$$ = $1
- $3;

}
| expr '&' expr {
$$ = $1 & $3;
}
| expr '|' expr {
$$ = $1 | $3;
}

| '
-' expr %prec UMINUS {
$$ =
-$2;
}
| LETTER {
$$ = regs[$1];
}
|

number : DIGIT {
$$ = $1;
base = ($1==0) ? 8 : 10;
}
| number DIGIT {
$$ = base * $1 + $2;
};
%%

int yyerror

(const char *s
)

{
fprintf(stderr, "%s
\n",s);

}

int yywrap() {
return(1);
}

int main() {
return(yyparse());