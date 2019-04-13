grammar Cymbol;



//Lexer
fragment TRUE      : 'true';
fragment FALSE     : 'false';
fragment NUMBER    : [0-9];
fragment LETTER    : [a-zA-Z];
fragment UNDERLINE : '_';

TYPEBOOL   : 'bool';
TYPEINT    : 'int';
TYPEVOID   : 'void';
TYPEFLOAT  : 'float';
TYPESTRING : 'string';

IF     : 'if';
ELSE   : 'else';
RETURN : 'return';

LP        : '(';
RP        : ')';
COMMA     : ',';
SEMICOLON : ';';
LB        : '{';
RB        : '}';

AS    : '=';
EQ    : '==';
NE    : '!=';
NOT   : '!';
GT    : '>';
LT    : '<';
GE    : '>=';
LE    : '<=';
MUL   : '*';
DIV   : '/';
PLUS  : '+';
MINUS : '-';

BOOL: (TRUE|FALSE);
ID  : (UNDERLINE | LETTER) (UNDERLINE | LETTER | NUMBER)*;
INT : NUMBER+;
FLOAT: NUMBER+'.'NUMBER+;
STRING: '"'(LETTER|NUMBER)*'"';


BLOCKCOMMENT : '/*' .*? '*/' -> skip;
LINECOMMENT  : '//' .*? '\n' -> skip;
WS           : [ \t\n\r]+ -> skip;



//Parser
fiile : (funcDecl | varDecl)+ EOF?
      ;

tyype : TYPEINT                                   #FormTypeInt
      | TYPEVOID                                  #FormTypeVoid
      | TYPEFLOAT                                 #FormTypeFloat
      | TYPESTRING                                #FormTypeString
      | TYPEBOOL                                  #FormTypeBool
      ;

funcDecl : functionType=tyype ID '('paramTypeList?')' block
         ;

varDecl : tyype ID ('=' expr)? ';'
        ;

paramTypeList : paramType (',' paramType)*
              ;

paramType : tyype ID
          ;

block : '{' stat* '}'
      ;

stat : varDecl
     | ifElseStat
     | returnStat
     | assignStat
     | exprStat
     ;

assignStat : ID '=' expr ';'
           ;

returnStat : RETURN expr? ';'
           ;

ifElseStat : ifStat (elseStat)?
           ;

ifElseExprStat : block 
               | ifElseStat
               | returnStat
               | assignStat
               | exprStat
               ;

exprStat : expr ';'
         ;

exprList : expr (',' expr)* 
         ;

ifStat : 'if' '(' expr ')' ifElseExprStat
       ;

elseStat : 'else' ifElseExprStat
         ;

expr : ID '(' exprList? ')'                                    #FunctionCallExpr
     | op=('+' | '-') expr                                     #SignedExpr
     | '!' expr                                                #NotExpr
     | expr op=('<' | '>' | '<=' | '>=' | '!=' | '==') expr    #ComparisonExpr
     | expr op=('*' | '/') expr                                #MulDivExpr
     | expr op=('+' | '-') expr                                #AddSubExpr
     | expr op=('&&' | '||') expr                              #AndOrExpr
     | ID                                                      #VarIdExpr
     | INT                                                     #IntExpr
     | FLOAT                                                   #FloatExpr
     | STRING                                                  #StringExpr
     | BOOL                                                    #BoolExpr
     | '(' expr ')'                                            #ParenExpr
     ;
