/*-***
 *
 * This file defines a stand-alone lexical analyzer for a subset of the Pascal
 * programming language.  This is the same lexer that will later be integrated
 * with a CUP-based parser.  Here the lexer is driven by the simple Java test
 * program in ./PascalLexerTest.java, q.v.  See 330 Lecture Notes 2 and the
 * Assignment 2 writeup for further discussion.
 *
 */


import java_cup.runtime.*;


/**
 * Thrown on input that cannot start any token. Line and column are 1-based.
 */
class ScannerException extends RuntimeException {
    ScannerException(String text, int line, int column) {
        super("Illegal char, '" + text + "' line: " + line + ", column: " + column);
    }
}


%%
/*-*
 * LEXICAL FUNCTIONS:
 */

%cup
%line
%column
%unicode
%class Lexer

%{

/**
 * Return a new Symbol with the given token id, and with the current line and
 * column numbers.
 */
Symbol newSym(int tokenId) {
    return new Symbol(tokenId, yyline, yycolumn);
}

/**
 * Return a new Symbol with the given token id, the current line and column
 * numbers, and the given token value.  The value is used for tokens such as
 * identifiers and numbers.
 */
Symbol newSym(int tokenId, Object value) {
    return new Symbol(tokenId, yyline, yycolumn, value);
}

%}


/*-*
 * PATTERN DEFINITIONS:
 */


/**
 * Implement patterns as regex here
 */

/**
 * Since I have no formal definitions of anything (unicode group for letter, number, etc. like Go Spec,
 * I will default to the ones in the example project)
 */

whitespace = [ \n\t\r]
digit = [0-9]
letter = [a-zA-Z]
inlinecomment = \\\\[^\n]*
blockcomment = \\\*([^*]|\*+[^\*\\])*\*+\\

intlit = {digit}+
floatlit = {digit}+\.{digit}+
id = {letter}({letter}|{digit})*

strlit = \"([^\"\n\t\\]|\\[tn\"\\])*\"
charlit = '([^'\t\n\\]|\\['\\tn])'

%%

/**
 * LEXICAL RULES:
 */

/**
 * Implement terminals here, ORDER MATTERS!
 */

/* Keyword */
class           {return newSym(sym.CLASS, yytext());}
final           {return newSym(sym.FINAL, yytext());}
void            {return newSym(sym.VOID, yytext());}
int             {return newSym(sym.INT, yytext());}
char            {return newSym(sym.CHAR, yytext());}
bool            {return newSym(sym.BOOL, yytext());}
float           {return newSym(sym.FLOAT, yytext());}
if              {return newSym(sym.IF, yytext());}
while           {return newSym(sym.WHILE, yytext());}
read            {return newSym(sym.READ, yytext());}
print           {return newSym(sym.PRINT, yytext());}
printline       {return newSym(sym.PRINTLINE, yytext());}
return          {return newSym(sym.RETURN, yytext());}
else            {return newSym(sym.ELSE, yytext());}
true            {return newSym(sym.TRUE, yytext());}
false           {return newSym(sym.FALSE, yytext());}

/* braces */
"(" {return newSym(sym.LPAREN, yytext());}
")" {return newSym(sym.RPAREN, yytext());}
"[" {return newSym(sym.LBRACKET, yytext());}
"]" {return newSym(sym.RBRACKET, yytext());}
"{" {return newSym(sym.LBRACE, yytext());}
"}" {return newSym(sym.RBRACE, yytext());}

/* operators and punctuation */
";"     {return newSym(sym.SEMICOLON, yytext());}
","     {return newSym(sym.COMMA, yytext());}
"?"     {return newSym(sym.QUESTION_MARK, yytext());}
":"     {return newSym(sym.COLON, yytext());}
"~"     {return newSym(sym.TILDE, yytext());}

"++"    {return newSym(sym.INCREMENT, yytext());}
"--"    {return newSym(sym.DECREMENT, yytext());}
"+"     {return newSym(sym.ADD, yytext());}
"-"     {return newSym(sym.SUB, yytext());}
"*"     {return newSym(sym.MUL, yytext());}
"/"     {return newSym(sym.DIV, yytext());}

"=="    {return newSym(sym.EQ, yytext());}
"="     {return newSym(sym.ASSIGN, yytext());}
"<="    {return newSym(sym.LTE, yytext());}
">="    {return newSym(sym.GTE, yytext());}
"<>"    {return newSym(sym.LTGT, yytext());}
"<"     {return newSym(sym.LT, yytext());}
">"     {return newSym(sym.GT, yytext());}

"||"    {return newSym(sym.LOR, yytext());}
"&&"    {return newSym(sym.LAND, yytext());}

/* Literals and Id */
{id}        {return newSym(sym.ID, yytext());}
{intlit}    {return newSym(sym.INTLIT, yytext());}
{floatlit}  {return newSym(sym.FLOATLIT, yytext());}
{charlit}   {return newSym(sym.CHARLIT, yytext());}
{strlit}    {return newSym(sym.STRLIT, yytext());}


{whitespace}    { /* Ignore whitespace. */ }
{inlinecomment} { /* Ignore comment. */ }
{blockcomment}  { /* Ignore block comment. */ }
[^]             { throw new ScannerException(yytext(), yyline + 1, yycolumn + 1); }
