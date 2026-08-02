%{
#include <stdio.h>

int linea = 1;


void imprimirToken(char *token)
{
    printf("Línea: %d\n", linea);
    printf("Token : %s\n", token);
    printf("Lexema: %s\n\n", yytext);
}
%}

%%

"var"      { imprimirToken("VAR"); }

"let"      { imprimirToken("LET"); }

"if"       { imprimirToken("IF"); }

"else"     { imprimirToken("ELSE"); }


\n         { linea++; }


[ \t]+     ;


.          ;

%%

int main()
{
    printf("===== ANALIZADOR LEXICO =====\n\n");

    yylex();

    printf("Fin del analisis \n");

    return 0;
}
