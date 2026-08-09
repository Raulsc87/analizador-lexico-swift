%{
#include <stdio.h>

int linea = 1;

int totalIdentificadores = 0;
int totalEnteros = 0;
int totalFlotantes = 0;
int totalBooleanos = 0;
int totalCadenas = 0;
int totalOperadores = 0;
int totalDelimitadores = 0;

FILE *archivoTokens;
FILE *tablaSimbolos;

void imprimirToken(char *token)
{
    printf("Línea: %d\n", linea);
    printf("Token : %s\n", token);
    printf("Lexema: %s\n\n", yytext);

    fprintf(archivoTokens, "%d\t%s\t%s\n", linea, token, yytext);
}
%}

%%

"var"       { imprimirToken("VAR"); }
"let"       { imprimirToken("LET"); }
"if"        { imprimirToken("IF"); }
"else"      { imprimirToken("ELSE"); }
"import"    { imprimirToken("IMPORT"); }
"func"      { imprimirToken("FUNC"); }
"return"    { imprimirToken("RETURN"); }
"struct"    { imprimirToken("STRUCT"); }
"class"     { imprimirToken("CLASS"); }
"init"      { imprimirToken("INIT"); }
"self"      { imprimirToken("SELF"); }
"while"     { imprimirToken("WHILE"); }
"for"       { imprimirToken("FOR"); }
"in"        { imprimirToken("IN"); }
"switch"    { imprimirToken("SWITCH"); }
"case"      { imprimirToken("CASE"); }
"default"   { imprimirToken("DEFAULT"); }

"true"      { totalBooleanos++; imprimirToken("BOOLEANO"); }
"false"     { totalBooleanos++; imprimirToken("BOOLEANO"); }

"=="        { totalOperadores++; imprimirToken("IGUAL_QUE"); }
"!="        { totalOperadores++; imprimirToken("DIFERENTE"); }
">="        { totalOperadores++; imprimirToken("MAYOR_IGUAL"); }
"<="        { totalOperadores++; imprimirToken("MENOR_IGUAL"); }

\=          { totalOperadores++; imprimirToken("ASIGNACION"); }
\>          { totalOperadores++; imprimirToken("MAYOR"); }
\<          { totalOperadores++; imprimirToken("MENOR"); }

\+          { totalOperadores++; imprimirToken("SUMA"); }
\-          { totalOperadores++; imprimirToken("RESTA"); }
\*          { totalOperadores++; imprimirToken("MULTIPLICACION"); }
\/          { totalOperadores++; imprimirToken("DIVISION"); }
\%          { totalOperadores++; imprimirToken("MODULO"); }
\!          { totalOperadores++; imprimirToken("NOT"); }

"+="        { totalOperadores++; imprimirToken("SUMA_ASIGNACION"); }
"-="        { totalOperadores++; imprimirToken("RESTA_ASIGNACION"); }
"*="        { totalOperadores++; imprimirToken("MULT_ASIGNACION"); }
"/="        { totalOperadores++; imprimirToken("DIV_ASIGNACION"); }

"&&"        { totalOperadores++; imprimirToken("AND"); }
"||"        { totalOperadores++; imprimirToken("OR"); }

"->"        { totalOperadores++; imprimirToken("FLECHA_RETORNO"); }

\(          { totalDelimitadores++; imprimirToken("PARENTESIS_ABRE"); }
\)          { totalDelimitadores++; imprimirToken("PARENTESIS_CIERRA"); }

\{          { totalDelimitadores++; imprimirToken("LLAVE_ABRE"); }
\}          { totalDelimitadores++; imprimirToken("LLAVE_CIERRA"); }

\[          { totalDelimitadores++; imprimirToken("CORCHETE_ABRE"); }
\]          { totalDelimitadores++; imprimirToken("CORCHETE_CIERRA"); }

\,          { totalDelimitadores++; imprimirToken("COMA"); }
\;          { totalDelimitadores++; imprimirToken("PUNTO_Y_COMA"); }
\:          { totalDelimitadores++; imprimirToken("DOS_PUNTOS"); }
\.          { totalDelimitadores++; imprimirToken("PUNTO"); }

\"([^\"\n]|\\.)*\" {
    totalCadenas++;
    imprimirToken("CADENA");
}

[a-zA-Z_][a-zA-Z0-9_]* {
    totalIdentificadores++;
    imprimirToken("IDENTIFICADOR");

    fprintf(tablaSimbolos,
            "%s\tIDENTIFICADOR\t%d\n",
            yytext,
            linea);
}

[0-9]+\.[0-9]+ {
    totalFlotantes++;
    imprimirToken("FLOTANTE");
}

[0-9]+ {
    totalEnteros++;
    imprimirToken("ENTERO");
}

\n {
    linea++;
}

[ \t]+ {
}

. {
}

%%

int main()
{
    printf("Analizador lexico \n\n");

    archivoTokens = fopen("tokens.txt", "w");

    if (archivoTokens == NULL)
    {
        printf("Error al crear tokens.txt\n");
        return 1;
    }

    tablaSimbolos = fopen("tabla_simbolos.txt", "w");

    if (tablaSimbolos == NULL)
    {
        printf("Error al crear tabla_simbolos.txt\n");
        return 1;
    }

    fprintf(tablaSimbolos, "LEXEMA\tTOKEN\tLINEA\n");

    yylex();

    printf("Fin del análisis.\n");

    printf("\nResumen\n");

    printf("Lineas: %d\n", linea);
    printf("Identificadores: %d\n", totalIdentificadores);
    printf("Enteros: %d\n", totalEnteros);
    printf("Flotantes: %d\n", totalFlotantes);
    printf("Booleanos: %d\n", totalBooleanos);
    printf("Cadenas: %d\n", totalCadenas);
    printf("Operadores: %d\n", totalOperadores);
    printf("Delimitadores: %d\n", totalDelimitadores);

    fclose(archivoTokens);
    fclose(tablaSimbolos);

    return 0;
}