run: link
	./calcu.exe

tab: 
	yacc -d calcu.y

lex: tab
	lex calcu.l

link: lex
	cc y.tab.c lex.yy.c -o calcu.exe

clean:
	rm -f *.lex *.exe *.calcu *.h *.c