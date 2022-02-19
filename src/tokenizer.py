"""
Transforms a string into a stream/list of tokens, while performing a basic syntax check
"""

from sys import stderr
from dataclasses import dataclass
from enum import auto, Enum
from typing import Union, Optional

Loc = tuple[ str, int, int ]
printToStderrOnFatalError: bool = False


class Keyword(Enum):
	# OP KEYWORDS
	IS = 'IS'
	OR = 'OTHRWIS'
	AND = 'FUTHRMOR'
	# CONTROL FLOW KEYWORDS
	IF = 'IF'
	ELSE = 'LS'
	DO = 'DO'
	CHECK = 'CHCK'
	UNTIL = 'UNTIL'
	WHEN = 'WHN'
	FINISHED = 'FINISHD'
	# NORMAL KEYWORDS
	DECLARE = 'DCLAR'
	CONSTANT = 'CONSTANT'
	VARIABLE = 'VARIABL'
	GIVE = 'GIV'
	BACK = 'BACK'
	SUBROUTINE = 'SUBROUTIN'
	CALL = 'CALL'
	EXPORT = 'XPORT'
	TEMPLATE = 'TMPLAT'
	BEHAVIOR = 'BHAVIOR'
	BUILD = 'BUILD'
	OWN = 'OWN'
	FROM = 'FROM'
	INITIALIZER = 'INITIALIZR'
	DEINITIALIZER = 'DINITIALIZR'
	# CONSTANTS
	ME = 'M'
	FALSE = 'NO'
	NOTHING = 'NOTHING'


class Symbol(Enum):
	LPAREN = '('
	RPAREN = ')'
	COLON = ':'
	COMMA = ','
	LBRACK = '['
	RBRACK = ']'
	LBRACE = '{'
	RBRACE = '}'
	EQUAL = '='
	SUB = '+'
	BANG = '!'
	DIV = ';'
	ADD = '-'
	MODULO = '\\'
	GT = '<'
	GE = '=<'
	DOT = '.'
	ARROW = '<-'


class UnaryType(Enum):
	SUBTRACT = auto()  # +
	ADD = auto()  # -
	DIVIDE = auto()  # ;
	MODULO = auto()  # \
	BANG = auto()  # !
	GREATER = auto()  # <
	GREATER_EQUAL = auto()  # =<
	BANG_IS = auto()  # !IS


class TokenType(Enum):
	NAME = auto()
	FLOAT = auto()
	STR = auto()
	KEYWORD = auto()
	SYMBOL = auto()
	UNARY = auto()
	EOF = auto()


@dataclass
class Token:
	typ: TokenType
	text: str
	loc: Loc
	value: Union[ float, str, Keyword, Symbol, UnaryType ]


@dataclass
class TokenizerError(Exception):
	message: Optional[str] = None


def parse(codeString: str, file: str) -> list[Token]:
	"""
	Parses a string of code into a list of tokens
	:param codeString: code string
	:param file: original file
	:return: list of tokens
	"""
	lines: list[str] = codeString.splitlines(True)
	code: list[Token] = []
	lineN: int = 0
	char: int = 0
	# work vars
	num: str

	def getChar() -> str:
		""" Returns and consume a char """
		nonlocal char
		return line[ ( char := char + 1 ) - 1 ] if char + 1 < len(line) else '\0'

	def peek( offset: int = 1 ) -> str:
		""" Returns a char """
		return line[ char + offset ] if char + offset < len(line) else '\0'

	def peekIgnoreSpaces( offset: int = 1 ) -> str:
		""" Returns a word """
		while peek(offset) == ' ':
			offset += 1
		return line[ char + offset ] if char + offset < len(line) else '\0'

	def getIsWord( word: str ) -> bool:
		""" Check if the next word is the give word """
		nonlocal char
		if line[ char : char + len(word) ] == word:
			char += len(word)
			return True
		return False

	def getLocation(word: str = '') -> Loc:
		""" Create a Location tuple """
		return file, lineN, char - ( len(word) - 1 )

	def assertIsKw(kw: Keyword, curr: Keyword, loc: Loc, offset: int = 0) -> None:
		"""
		Raises a fatal exception if the token at $offset is not the given keyword
		:param kw: Expected keyword
		:param curr: Current keywordthat requires the check
		:param loc: Current keyword's location tuple
		:param offset: Offset to check
		:raises TokenizerError: When the token is wrong
		"""
		if len(code) == 0 or code[ -1 + offset ].typ != TokenType.KEYWORD or code[ -1 + offset ].value != kw:
			fatal(
				f'Missing {kw.name} keyword before {curr.name} keyword at line ' '{line} column {char}',
				loc[1],
				loc[2]
			)

	def fatal(message: str, lineNum: int, col: int) -> None:
		"""
		Raise an exception with debug information
		:param message: Message of the exception
		:param lineNum: Line where the error originated
		:param col: Column where the error originated
		"""
		err = f'ERROR: File "{file}", line { lineNum + 1 } - {message.format(line=lineNum + 1, char=col)}\n'
		err += lines[lineNum] + '\n'
		err += ( ' ' * ( col - 1 ) ) + '^ here'
		if printToStderrOnFatalError:
			print( err, file=stderr )
		raise TokenizerError(err)

	# execute until there are no more lines
	while lineN < len(lines):
		line = lines[lineN]

		if getIsWord('DCLAR'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('DCLAR'), Keyword.DCLAR ) ]
		elif getIsWord('SUBROUTIN'):
			if len(code) == 0:
				fatal('Expected DCLAR SUBROUTIN, found SUBROUTIN at line {line}', lineN, 0 )
			elif code[-1].typ != TokenType.KEYWORD and code[-1].value != Keyword.DCLAR and line[char + 2] != '[':
				fatal('Expected DCLAR SUBROUTIN, found SUBROUTIN at line {line}', lineN, char )
			code += [ Token( TokenType.KEYWORD, '', getLocation('SUBROUTIN'), Keyword.SUBROUTIN ) ]
		elif getIsWord('CONSTANT'):
			assertIsKw( Keyword.DCLAR, Keyword.CONSTANT, getLocation('CONSTANT') )
			code += [ Token( TokenType.KEYWORD, '', getLocation('CONSTANT'), Keyword.CONSTANT ) ]
		elif getIsWord( 'VARIABL' ):
			assertIsKw( Keyword.DCLAR, Keyword.VARIABL, getLocation('VARIABL') )
			code += [ Token( TokenType.KEYWORD, '', getLocation( 'VARIABL' ), Keyword.VARIABL ) ]
		elif getIsWord('CALL'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('CALL'), Keyword.CALL ) ]
		elif getIsWord('BUILD'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('BUILD'), Keyword.BUILD ) ]
		elif getIsWord('OWN'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('OWN'), Keyword.OWN ) ]
		elif getIsWord('XPORT'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('XPORT'), Keyword.XPORT ) ]
		elif getIsWord('TMPLAT'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('TMPLAT'), Keyword.TMPLAT ) ]
		elif getIsWord('FROM'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('FROM'), Keyword.FROM ) ]
		elif getIsWord('GIV'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('GIV'), Keyword.GIV ) ]
		elif getIsWord('WHIL'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('WHIL'), Keyword.WHIL ) ]
		elif getIsWord('BACK'):
			assertIsKw( Keyword.GIV, Keyword.BACK, getLocation('BACK') )
			code += [ Token( TokenType.KEYWORD, '', getLocation('BACK'), Keyword.BACK ) ]
		elif getIsWord( 'IS' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation( 'IS' ), Keyword.IS ) ]
		elif getIsWord( 'CHCK' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation( 'CHCK' ), Keyword.CHCK ) ]
		elif getIsWord( 'IF' ):
			assertIsKw( Keyword.CHCK, Keyword.IF, getLocation( 'IF' ) )
			code += [ Token( TokenType.KEYWORD, '', getLocation( 'IF' ), Keyword.IF ) ]
		elif getIsWord(','):
			if peek(0) in '0123456789':
				# leading dot float
				num = '.'
				while peek( 0 ) in '1234567890':
					num += getChar()
				fnum = float( num )
				code += [ Token( TokenType.FLOAT, '', getLocation( str( fnum ) ), fnum ) ]
				continue
			code += [ Token( TokenType.KEYWORD, '', getLocation(','), Keyword.Comma ) ]
		elif getIsWord('='):
			code += [ Token( TokenType.KEYWORD, '', getLocation('='), Keyword.Equal ) ]
		elif getIsWord('.'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('.'), Keyword.Dot ) ]
		elif getIsWord( '{' ):
			if (
					len( code ) == 0 or
					peekIgnoreSpaces() not in ',1234567890'
			):
				if (
					len( code ) == 0 or (
						code[-1].value != Keyword.SUBROUTIN and
						code[-1].value != Keyword.BracketClose and
						code[-1].value != Keyword.IF and
						code[-1].value != Keyword.CALL and
						code[-1].typ != TokenType.NAME
					)
				):
					fatal(
						'at {line}:{char} opening brace can only go after a name, a SUBROUTIN, a IF, a ] keyword or before an expression',
						lineN,
						char
					)
			if (
					(
							len(code) < 2 and
							len( code ) != 0 and
							peek() not in ',1234567890'
					) or (
						len( code ) != 0 and
						peek() not in ',1234567890' and
						code[-1].typ == TokenType.NAME and
						code[-2].value != Keyword.CALL and
						code[-2].value != Keyword.BUILD and
						code[-2].value != Keyword.Comma and
						code[-2].value != Keyword.IF and
						code[-2].value != Keyword.SUBROUTIN
					)
			):
				fatal(
					'missing SUBROUTIN or CALL keyword at {line}:{char}',
					code[-1].loc[1],
					code[-1].loc[2]
				)
			code += [ Token( TokenType.KEYWORD, '', getLocation('{'), Keyword.CurlyOpen ) ]
		elif getIsWord( '}' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation('}'), Keyword.CurlyClose ) ]
		elif getIsWord( '[' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation('['), Keyword.BracketOpen ) ]
		elif getIsWord( ']' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation(']'), Keyword.BracketClose ) ]
		elif getIsWord( '(' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation('('), Keyword.ParenthesesOpen ) ]
		elif getIsWord( ')' ):
			code += [ Token( TokenType.KEYWORD, '', getLocation(')'), Keyword.ParenthesesClose ) ]
		elif getIsWord('<-'):
			assertIsKw( Keyword.CurlyClose, Keyword.Arrow, getLocation('<-') )
			code += [ Token( TokenType.KEYWORD, '', getLocation('<-'), Keyword.Arrow ) ]
		elif getIsWord('/'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('/'), Keyword.Slash ) ]
		elif getIsWord('+'):
			code += [ Token( TokenType.UNARY, '', getLocation('+'), UnaryType.SUBTRACT ) ]
		elif getIsWord('-'):
			code += [ Token( TokenType.UNARY, '', getLocation('-'), UnaryType.ADD ) ]
		elif getIsWord(';'):
			code += [ Token( TokenType.UNARY, '', getLocation(';'), UnaryType.DIVIDE ) ]
		elif getIsWord('!IS'):
			code += [ Token( TokenType.UNARY, '', getLocation('!IS'), UnaryType.BANG_IS ) ]
		elif getIsWord('!'):
			code += [ Token( TokenType.UNARY, '', getLocation('!'), UnaryType.BANG ) ]
		elif getIsWord('\\'):
			code += [ Token( TokenType.UNARY, '', getLocation('\\'), UnaryType.MODULO ) ]
		elif getIsWord(' '):
			pass
		elif getIsWord('\n') or char == len(line) - 1:
			if (
					code[-1].typ != TokenType.KEYWORD or
					code[-1].value not in ( Keyword.Slash, Keyword.BracketOpen, Keyword.BracketClose )
			) and len(line) != 2:
				fatal(
					'Missing "/" before newline at line {line} column {char}',
					lineN,
					char
				)
			lineN += 1
			char = 0
		elif getIsWord('\0') or ( char == len( line ) and lineN == len(lines) - 1 ):
			break
		elif getIsWord('|*'):
			startLine: int = lineN
			found = False
			chIndex = 0
			while lineN < len(lines) and not found:
				chLine = lines[lineN]
				chIndex = 0
				while chIndex < len( chLine ):
					if chLine[chIndex] == '*' and chLine[chIndex + 1] == '|':
						found = True
						break
					chIndex += 1
				if not found:
					lineN += 1
			else:
				if not found:
					fatal(
						'Reached end of file, expected "*|" after comment at line {line}',
						startLine,
						chIndex + 1
					)
			if startLine == lineN:
				fatal(
					'Comments must be at least 2 lines long. line {line}',
					startLine,
					chIndex + 1
				)
			lineN += 1
			char = 0
		elif getIsWord('*'):
			string: str = ''
			while peek(0) != '*':
				if peek(0) == '\n':
					fatal(
						'Reached end of line ({line}) without closing string "*"',
						lineN,
						char
					)
				string += getChar()
			char += 1
			code += [ Token( TokenType.STR, string, getLocation(string), string ) ]
		elif peek(0) in ',1234567890':
			num = ''
			while peek(0) in ',1234567890':
				if ( numChar := getChar() ) != '\0':
					num += numChar
				else:
					fatal(
						'Reached end of line without ending /',
						lineN,
						char + len(num)
					)
			fnum = float( num.replace(',', '.') )
			code += [ Token( TokenType.FLOAT, '', getLocation( str( fnum ) ), fnum ) ]
		else:
			name: str = ''
			while peek(0) not in (' ', '\n', '{', '(', '[', ']', ')', '}', '.', '\0', '/'):
				name += getChar()
			if 'e' in name.lower() and ( code[-1].typ != TokenType.KEYWORD or code[-1].value != Keyword.FROM ):
				fatal(
					'the name at line {line} and column {char} contains "e"',
					lineN,
					char - ( len(name) - 1 ) + name.lower().index('e')
				)
			code += [ Token( TokenType.NAME, name, getLocation(name), name ) ]
	return code


if __name__ == '__main__':
	from time import time
	from pathlib import Path
	from pprint import pprint
	from sys import argv

	from utils import ExitError

	start = time()
	exitCode = 0
	try:
		pprint(
			parse(
				Path( argv[1] ).read_text(),
				argv[1]
			)
		)
	except ExitError as e:
		exitCode = e.code

	print(f'Done in {time() - start}')
	exit(exitCode)
