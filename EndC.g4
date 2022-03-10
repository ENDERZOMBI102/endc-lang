grammar EndC;

/** The start rule must be whatever you would normally use, such as script
 *  or compilationUnit, etc...
 */
script
	:	import_statement* ( vardef | function | statement | template )+ EOF
	;

// IMPORT
import_statement
	:	OWN importables FROM IDENTIFIER '/'
	;

importables : importable ( '.' importable )* ;

importable : IDENTIFIER ;

// DECLARATIONS
function
	:	EXPORT? DECLARE SUBRUTINE IDENTIFIER func_args ARROWL type func_block
	;

method
	:	DECLARE BEHAVIOR IDENTIFIER func_args ARROWL type func_block
	;

template
	:	EXPORT? DECLARE TEMPLATE IDENTIFIER template_block
	;

template_initializer
	: DECLARE INITIALIZER func_args func_block
	;

template_deinitializer
	: DECLARE DEINITIALIZER func_args func_block
	;

vardef
	:	DECLARE CONSTANT type IDENTIFIER '=' expr '/'					# DeclareConstant
	|	DECLARE VARIABLE type IDENTIFIER ( '=' expr )? '/'				# DeclareVariable
	;

// ARGUMENTS
func_args : '{' formal_args? '}' ;

formal_args : formal_arg ('.' formal_arg)* ;

formal_arg : type IDENTIFIER ;

arguments : '{' expr_list? '}' ;

// BLOCKS
template_block
	:	'['
			(	vardef
			| 	method
			| 	template_initializer
			|	template_deinitializer
			)+
		']'
	;

func_block :  '[' (statement|vardef)* ']' ;

statement
	:	CHECK IF '{' expr '}' DO func_block ( ELSE DO func_block )?	'/'						# If
	|	CHECK UNTIL '{' expr '}' DO func_block ( WHEN FINISHED DO func_block )?	'/'			# Until
	|	DO func_block UNTIL WHEN '{' expr '}' ( WHEN FINISHED DO func_block )?	'/'			# DoUntil
	|	qualified_name '=' expr '/'															# Assign
	|	qualified_name '(' expr ')' '=' expr '/'											# ElementAssign
	|	call_expr '/'																		# CallStatement
	|	GIVE BACK expr '/'																	# Return
	|	func_block '/'				 														# BlockStatement
	|	DECLARE SECTION ASM '{' backends '}' asm_block '/'									# BlockAsm
	;

// EXPRESSIONS
expr
	:	expr operator expr									# Op
	|	ADD expr											# Negate
	|	BANG expr											# Not
	|	call_expr											# Call
	|	qualified_name '(' expr ')'							# Index
	|	'{' expr '}'										# Parens
	|	primary												# Atom
	|	anonim_function										# AnonimFunction
	;

anonim_function	: SUBRUTINE func_args ARROWL type func_block ;

call_expr
	: CALL qualified_name arguments									# SimpleCall
	| CALL BUILD IDENTIFIER arguments								# TemplateInstantiation
	| CALL '{' call_expr '}' ARROWR qualified_name arguments		# NestedCall
	| CALL anonim_function arguments								# DirectCall
	;

expr_list : expr ('.' expr)* ;

// OTHA
primary
	:	qualified_name										# Identifier
	|	INT													# Integer
	|	FLOAT												# Float
	|	STRING												# String
	|	NOTHING												# Nothing
	|	'(' expr_list ')'									# Vector
	|	FALSE												# FalseLiteral
	|	ME													# MetaConstant
	;

type
	:	'InTgR'                                             # IntTypeSpec
	|	'StRiNg'                                            # StringTypeSpec
	|	'BoOlAn'											# BooleanTypeSpec
	|	'NoThInG'											# NothingTypeSpec
	|	type '()'											# ArrayTypeSpec
	|	IDENTIFIER											# CustomTypeSpec
	;

qualified_name : IDENTIFIER ( ARROWR IDENTIFIER )* ;

operator : SUB|DIV|ADD|MODULO|GT|GE|IS|OR|AND|ARROWR ; // no implicit precedence


backends : DOTNET|LLVM|WASM|NEKO|HASHLINK|JVM|PYTHON|JAVASCRIPT ;

asm_block : '[' (.^\])*? ']' ;


// SYMBOLS
LPAREN : '(' ;
RPAREN : ')' ;
LBRACK : '[' ;
RBRACK : ']' ;
LBRACE : '{' ;
RBRACE : '}' ;
COLON : ':' ;
COMMA : ',' ;
EQUAL : '=' ;
SUB : '+' ;
BANG : 'ඞ' ;
DIV : ';' ;
ADD : '-' ;
MODULO : ';' ;  // greek question mark
GT : '<' ;
GE : '=<' ;
DOT : '.' ;
ARROWL : '<-' ;
ARROWR : '->' ;

// KEYWORDS
// OP KEYWORDS
IS : 'IS' ;
OR : 'OTHRWIS' ;
AND : 'FUTHRMOR' ;
// CONTROL FLOW KEYWORDS
IF : 'IF' ;
ELSE : 'LS' ;
DO : 'DO' ;
CHECK : 'CHCK' ;
UNTIL : 'UNTIL' ;
WHEN : 'WHN' ;
FINISHED : 'FINISHD' ;
// NORMAL KEYWORDS
DECLARE : 'DCLAR' ;
CONSTANT : 'CONSTANT' ;
VARIABLE : 'VARIABL' ;
GIVE : 'GIV' ;
BACK : 'BACK' ;
SUBRUTINE : 'SUBROUTIN' ;
CALL : 'CALL' ;
EXPORT : 'XPORT' ;
TEMPLATE : 'TMPLAT' ;
BEHAVIOR : 'BHAVIOR' ;
BUILD : 'BUILD' ;
OWN : 'OWN' ;
FROM : 'FROM' ;
INITIALIZER : 'INITIALIZR' ;
DEINITIALIZER : 'DINITIALIZR' ;
SECTION : 'SCTION' ;
ASM : 'ASM' ;
// BACKENDS
DOTNET : 'DOTNET' ;
LLVM : 'LLVM' ;
WASM : 'WASM' ;
NEKO : 'NEKO' ;
HASHLINK : 'HASHLINK' ;
JVM : 'JVM' ;
PYTHON : 'PYTHON' ;
JAVASCRIPT : 'JAVASCRIPT' ;
// CONSTANTS
ME : 'M' ;
FALSE : 'NO' ;
NOTHING : 'NOTHING' ;

// DYNAMIC NAMES
COMMENT : '|*' .*? '*|' -> channel(HIDDEN) ;

IDENTIFIER : [a-zA-Z_]([a-zA-Z0-9_])+ ;
INT : [0-9]+ ;
FLOAT
	:   '-'? INT COMMA INT EXP?   // 1.35, 1.35E-9, 0.3, -4.5
	|   '-'? INT EXP            // 1e10 -3e4
	|	'-'? COMMA INT
	;
fragment EXP :   [Ee] [+\-]? INT ;

STRING :  '*' ( '\\*' | . )*? '*' ;
fragment ESC :   '\\' [\bfnrt] ;

NEWLINE : [ \n\r]+ -> channel(HIDDEN) ;
TAB : [\t]+ ;
SPACE : ([ ]{5})*[^ ] ;

/** "catch all" rule for any char not matche in a token rule of your
 *  grammar. Lexers in Intellij must return all tokens good and bad.
 *  There must be a token to cover all characters, which makes sense, for
 *  an IDE. The parser however should not see these bad tokens because
 *  it just confuses the issue. Hence, the hidden channel.
 */
ERRCHAR
	:	.	-> channel(HIDDEN)
	;
