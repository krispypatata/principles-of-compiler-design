exer3:
	lex GABINETEKG_exer3.l
	cc lex.yy.c -o GABINETEKG_exer3.out -lfl
	./line_count GABINETEKG_exer3_input.txt

sample:
	lex line_count.l
	cc lex.yy.c -o line_count.out -lfl
	./line_count sample_input.txt

clean:
	rm -f *.out