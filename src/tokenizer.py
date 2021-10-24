from sys import stderr
from dataclasses import dataclass
from enum import auto, Enum
from typing import Union

Loc = tuple[ str, int, int ]
printToStderrOnFatalError: bool = False


class Keyword(Enum):
	# KEYWORDS
	DCLAR = auto()  # DCLAR
	CALL = auto()  # CALL
	FUNC = auto()  # FUNC
	CHCK = auto()  # CHCK
	IF = auto()  # IF
	Doc = auto()  # DO
	LS = auto()  # LS
	IS = auto()  # IS
	CONSTANT = auto()  # CONSTANT
	VARIABL = auto()  # VARIABL
	OWN = auto()  # OWN
	FROM = auto()  # FROM
	XPORT = auto()  # XPORT
	GIV = auto()  # GIV
	BACK = auto()  # BACK
	TMPLAT = auto()  # TMPLAT
	WHIL = auto()  # WHIL
	# COMMENTS
	CommentOpen = auto()  # |*
	CommentText = auto()  # |* THIS TEXT *|
	CommentClose = auto()  # *|
	# PARENTHESES
	BracketOpen = auto()  # [
	BracketClose = auto()  # ]
	CurlyOpen = auto()  # {
	CurlyClose = auto()  # }
	ParenthesesOpen = auto()  # (
	ParenthesesClose = auto()  # )
	# SYMBOLS
	Slash = auto()  # /
	Arrow = auto()  # <-
	Dot = auto()  # .
	Comma = auto()  # ,
	Equal = auto()  # =
	Newline = auto()  # \n
	# BUILTIN VALUES
	NO = 'NO'
	NOTHING = 'NOTHING'


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
	UNARY = auto()
	EOF = auto()


@dataclass
class Token:
	typ: TokenType
	text: str
	loc: Loc
	value: Union[float, str, Keyword, UnaryType]


class TokenizerError(Exception):
	pass


def parse(codeString: str, file: str) -> list[Token]:
	lines: list[str] = codeString.splitlines(True)
	code: list[Token] = []
	lineN: int = 0
	char: int = 0
	# work vars
	num: str

	def getChar() -> str:
		nonlocal char
		return line[ ( char := char + 1 ) - 1 ] if char + 1 < len(line) else '\0'

	def peek( offset: int = 1 ) -> str:
		return line[ char + offset ] if char + offset < len(line) else '\0'

	def getIsWord( word: str ) -> bool:
		nonlocal char
		if line[ char : char + len(word) ] == word:
			char += len(word)
			return True
		return False

	def getLocation(word: str = '') -> Loc:
		return file, lineN, char - ( len(word) - 1 )

	def assertIsKw(kw: Keyword, curr: Keyword, loc: Loc, offset: int = 0) -> None:
		if len(code) == 0 or code[ -1 + offset ].typ != TokenType.KEYWORD or code[ -1 + offset ].value != kw:
			fatal(
				f'Missing {kw.name} keyword before {curr.name} keyword at line ' '{line} column {char}',
				loc[1],
				loc[2]
			)

	def fatal(message: str, lineNum: int, col: int) -> None:
		err = f'ERROR: File "{file}", line { lineNum + 1 } - {message.format(line=lineNum + 1, char=col)}\n'
		err += lines[lineNum] + '\n'
		err += ( ' ' * ( col - 1 ) ) + '^ here'
		if printToStderrOnFatalError:
			print( err, file=stderr )
		raise TokenizerError(err)

	while lineN < len(lines):
		line = lines[lineN]

		if getIsWord('DCLAR'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('DCLAR'), Keyword.DCLAR ) ]
		elif getIsWord('FUNC'):
			if len(code) == 0:
				fatal('Expected DCLAR FUNC, found FUNC at line {line}', lineN, 0 )
			elif code[-1].typ != TokenType.KEYWORD and code[-1].value != Keyword.DCLAR and line[char + 2] != '[':
				fatal('Expected DCLAR FUNC, found FUNC at line {line}', lineN, char )
			code += [ Token( TokenType.KEYWORD, '', getLocation('FUNC'), Keyword.FUNC ) ]
		elif getIsWord('CONSTANT'):
			assertIsKw( Keyword.DCLAR, Keyword.CONSTANT, getLocation('CONSTANT') )
			code += [ Token( TokenType.KEYWORD, '', getLocation('CONSTANT'), Keyword.CONSTANT ) ]
		elif getIsWord( 'VARIABL' ):
			assertIsKw( Keyword.DCLAR, Keyword.VARIABL, getLocation('VARIABL') )
			code += [ Token( TokenType.KEYWORD, '', getLocation( 'VARIABL' ), Keyword.VARIABL ) ]
		elif getIsWord('CALL'):
			code += [ Token( TokenType.KEYWORD, '', getLocation('CALL'), Keyword.CALL ) ]
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
			if len( code ) < 1:
				fatal(
					'at {line}:{char} opening bracket cannot open an expression/statement',
					lineN,
					char
				)
			if (
					code[-1].value != Keyword.FUNC and
					code[-1].value != Keyword.BracketClose and
					code[-1].value != Keyword.IF and
					code[-1].typ != TokenType.NAME
			):
				fatal(
					'at {line}:{char} opening bracket can only go after a name, a FUNC, a IF or a ] keyword',
					lineN,
					char
				)
			if (
					code[-1].typ == TokenType.NAME and
					code[-2].value != Keyword.CALL and
					code[-2].value != Keyword.IF and
					code[-2].value != Keyword.FUNC
			):
				fatal(
					'missing FUNC or CALL keyword at {line}:{char}',
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
				num += getChar()
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
