%{
    /*
    Gabinete, Keith Ginoel S.
    March 31, 2025
    CMSC 129 - CD-1L
    */

    #include <stdio.h>
    #include <string.h>
    #include <stdlib.h>
    #include "y.tab.h"

    extern YYSTYPE yylval;
%}

%%
[ \t] ; /* Ignore spaces */

[a-z] {
    yylval.num = yytext[0] - 'a';
    return(LETTER);
}

[0-9] {
    yylval.num = yytext[0] - '0';
    return(DIGIT);
}

[^a-z0-9\b] {
    return yytext[0];
}

print\(\"([^\"\n]*)\"\) {
    /* Double-quoted string */
    yylval.str = strdup(yytext + 7);
    yylval.str[strlen(yylval.str) - 2] = '\0';
    return PRINT;
}

print\(\'([^\'\n]*)\'\) {
    /* Single-quoted string */
    yylval.str = strdup(yytext + 7);
    yylval.str[strlen(yylval.str) - 2] = '\0';
    return PRINT;
}

^[ \t]*"exit\(\)"[ \t]*$ {return QUIT;}
%%
