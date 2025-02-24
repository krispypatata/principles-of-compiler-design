/* Gabinete, Keith Ginoel S. */
/* CMSC 129 - CD-1L */ 
/* February 24, 2025 */

%%
(\.\-) printf("A");
(\-\.\.\.) printf("B");
(\-\.\-\.) printf("C");
(\-\.\.) printf("D");
(\.) printf("E");
(\.\.\-\.) printf("F");
(\-\-\.) printf("G");
(\.\.\.\.) printf("H");
(\.\.) printf("I");
(\.\-\-\-) printf("J");
(\-\.\-) printf("K");
(\.\-\.\.) printf("L");
(\-\-) printf("M");
(\-\.) printf("N");
(\-\-\-) printf("O");
(\.\-\-\.) printf("P");
(\-\-\.\-) printf("Q");
(\.\-\.) printf("R");
(\.\.\.) printf("S");
(\-) printf("T");
(\.\.\-) printf("U");
(\.\.\.\-) printf("V");
(\.\-\-) printf("W");
(\-\.\.\-) printf("X");
(\-\.\-\-) printf("Y");
(\-\-\.\.) printf("Z");

(\-\-\-\-\-) printf("0");
(\.\-\-\-\-) printf("1");
(\.\.\-\-\-) printf("2");
(\.\.\.\-\-) printf("3");
(\.\.\.\.\-) printf("4");
(\.\.\.\.\.) printf("5");
(\-\.\.\.\.) printf("6");
(\-\-\.\.\.) printf("7");
(\-\-\-\.\.) printf("8");
(\-\-\-\-\.) printf("9");

(\.\-\-\-\-\.) printf("'");

(\.\.\.\.\.\.) printf(" ");

%%
int main(int argc, char *argv[]) {
    yyin = fopen(argv[1], "r");
    yylex();
    fclose(yyin);
}
