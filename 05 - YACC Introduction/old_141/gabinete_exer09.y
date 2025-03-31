/*simplest version of calculator: from O'Reilly Media, Inc. 2021*/
/*
  Gabinete, Keith Ginoel S.
  CMSC 141 - D1L
  Exercise No. 9 - Introduction to lex|flex and yacc|bison for language translators
*/
/*
  %code requires...
  fixes the problem where input type (YYSTYPE) is limited to 'integer' only
  I found the solution here: <https://stackoverflow.com/questions/14462808/flex-bison-interpreting-numbers-as-floats>
  Now, I can perform arithmetic operations with floating point numbers
*/
%code requires
{
  #define YYSTYPE float
}

%{  // Section 1a: C declarations
  #include<stdio.h>
  #include<math.h>    // for pow() function; also need to add '-lm' when compiling
  // for bonus part
  #include<stdbool.h> 
  #include<stdlib.h>
  #include<string.h>

  int yylex();
  void yyerror(char *s);

  // for bonus part
  // handling multiple variable assignments
  typedef struct var_tag{
    char var_name[100];
    float value;
    struct var_tag* next;
  } VAR;

  // variable list (stack implementation)
  typedef struct list_tag {
    VAR *head;
  } VAR_LIST;

  // global variable list
  VAR_LIST *L;

  // methods
  void assign_variable(char *variable_name, float value, bool var_exists);
  bool check_if_variable_exists(char *variable_name);
  float get_value(char *variable_name);
%}

// Section 1b: YACC/Bison declarations
/*declare tokens*/
%token VAR_NAME ASS
%token INTEGER FLOAT
%token ADD SUB MUL DIV
%token NEG POW
%token EOL QUIT

/*
  references:
  <https://www.baeldung.com/cs/infix-prefix-postfix#:~:text=The%20prefix%20and%20postfix%20notations,postfix%20notations%20require%20special%20handling.>
  <https://www.geeksforgeeks.org/evaluation-prefix-expressions/>
      I learned from the articles above that, in evaluating arithmetic operations in prefix notation, 
  we don't have to follow any operator precedence rule. However, there is still a general rule to follow
  ;that is - the operator should always come first before the operands.
      So in contrast with the setup in infix calculator where we create several nonterminal symbols to 
  maintain multiple operator precedence rules, here in prefix calculator we can just create one nonterminal
  symbol for all the operations/ mathematical expressions we wish to evaluate since any of them can go first and
  each operation instruction only maintains the form: 
      <operator> <operand1> <operand2>;
      or <operator> <operand1> // for negation
      where operands 1 and/or 2 can be an expression
*/

%%  // Section 2: Grammar rules
calclist: /*nothing*/		    //matches at beginning of input
  | calclist exp EOL       {printf("=%f\n", $2);} //EOL is end of an expression
  | calclist QUIT          {printf("Exiting...\n"); return 0;}  // exit the program
  ;
/*exp = nonterminal symbol for all operations*/
exp:
    ADD exp exp            {$$ = $2 + $3;}
  | SUB exp exp            {$$ = $2 - $3;}
  | MUL exp exp            {$$ = $2 * $3;}
  | DIV exp exp            {$$ = $2 / $3;}

  | NEG exp                {$$ = $2 * -1;}      // unary minus '!'

  /*restricted to integer exponents only; also need to add '-lm' (due to math.h library) when compiling*/
  /*check if the second operand is int <https://stackoverflow.com/questions/5796983/checking-if-float-is-an-integer>*/
  | POW exp exp            { if ($3 - (int) $3 == 0) $$ = pow($2, $3);  else yyerror("not an integer exponent!");} 

  // for bonus part (handling multiple variable assignments (one-letter variables only))
  | ASS VAR_NAME exp       {
    char var_name[100];
    sprintf(var_name, "%f", $2);
    assign_variable(var_name, $3, check_if_variable_exists(var_name));
  }           

  /*terminal symbols*/
  | INTEGER                //default $$ = $1
  | FLOAT                  //default $$ = $1
  | VAR_NAME               {
    char var_name[100];
    sprintf(var_name, "%f", $1);
    if (check_if_variable_exists(var_name)) $$ = get_value(var_name);
    else yyerror("variable does not exist!");
  }
  ;
%%


// Section 3: Additional C code
/*
  creating or updating variable assignment (if the variable already exists in the list)
*/
void assign_variable(char *variable_name, float value, bool var_exists) {
  if (var_exists==false) {
    // creating a variable
    VAR *temp = (VAR *)malloc(sizeof(VAR));
    temp->next=NULL;
    strcpy(temp->var_name, variable_name);
    temp->value=value;

    // insert at head
    if (L->head == NULL) L->head = temp;
    else {
      temp->next = L->head;
      L->head = temp;
    }
  } else {
    // if var exists, just update its value
    VAR *temp = L->head;
    while (temp!=NULL) {
      if (strcmp(temp->var_name, variable_name) == 0) {
        temp->value = value;
      }
      temp = temp->next;
    }
  }

}

/*
  for checking if the variable name entered by the user exists in our storage of variables
*/
bool check_if_variable_exists(char *variable_name) {
  // traverse through the contents of the list
  if (L->head != NULL) {
    VAR *temp = L->head;
    while (temp!=NULL) {
      // if found
      if (strcmp(temp->var_name, variable_name) == 0) {
        return true;
      }
      temp = temp->next;
    }
  }

  // if not found
  return false;
}

/*
  for getting the value of a certain variable
*/
float get_value(char *variable_name) {
  VAR *temp = L->head;
  // traverse through the contents of the list
  while (temp!=NULL) {
    // if variable is found, return the value
    if (strcmp(temp->var_name, variable_name) == 0) {
      return temp->value;
    }
    temp = temp->next;
  }

  return 0;
}

void yyerror(char *s){
  fprintf(stderr, "error: %s\n", s);
}

int main(int argc, char **argv){
  // initialize a variable list
  L = (VAR_LIST *) malloc(sizeof(VAR_LIST));
  L->head = NULL;

  yyparse();
  return 0;
}

/*
BASIS : Infix Version

// Section 2: Grammar rules
calclist: // nothing	//matches at beginning of input
| calclist exp EOL 		{printf("=%f\n", $2); } //EOL is end of an expression
| calclist QUIT 			{printf("Exitting...\n"); return 0;}
;

exp: factor 				        //default $$ = $1
  | exp ADD factor 			    {$$ = $1 + $3;}
  | exp SUB factor 			    {$$ = $1 - $3;}
  ;

factor: negation				    //default $$ = $1
  | factor MUL negation 		{$$ = $1 * $3;}
  | factor DIV negation 		{$$ = $1 / $3;}
  ;

// supports repeated negation (ex. !!!!!2 = -2)
negation: exponent
  | negations exponent      {$$ = $2 * $1;}
  ;

negations: NEG              {$$ = -1;}
  | negations NEG           {$$ = $$ * -1;}
  ;

// uses the pow() function from math.h library; need to add '-lm' when compiling
// restricted to integer exponents only (either positive or negative)
// also supports repeated negation on the exponent
exponent: term
  | exponent POW INTEGER              {$$ = pow($1, $3);}             // positive integer as exponent
  | exponent POW negations INTEGER    {$$ = pow($1, $4 * $3);}        // negative integer as exponent
  ;

term: INTEGER               //default $$ = $1
  | FLOAT 				
  ;

*/
