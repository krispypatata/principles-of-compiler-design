%{
#include <stdio.h>
#include <string.h>
#include "y.tab.h"
int c;
extern int yylval;
char *string;
%}
%%
" " ;
[a-z] {
    c = yytext[0];
    yylval = c - 'a';
    return(LETTER);
}

[0-9] {
    c = yytext[0];
    yylval = c - '0';
    return(DIGIT);
}
[^a-z0-9\b] {
    c = yytext[0];
    return(c);
}
print\(\"(\\.|[^\"])*\"\) {
    string = strdup(yytext+7);
    printf("%s\n", strlen(string), string);
    return PRINT;
    // return yytext[0];
    // return QUIT;
}

exit {return QUIT;}
%%