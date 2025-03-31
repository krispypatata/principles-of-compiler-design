FILENAME := GABINETEKG_exer5

run: link
	./${FILENAME}.exe

tab: 
	yacc -d ${FILENAME}.y

lex: tab
	lex ${FILENAME}.l

link: lex
	cc y.tab.c lex.yy.c -o ${FILENAME}.exe

clean:
	rm -f *.lex *.exe *.${FILENAME} *.h *.c