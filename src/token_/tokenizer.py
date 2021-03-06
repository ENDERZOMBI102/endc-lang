"""
Transforms a string into a stream/list of tokens, while performing a basic syntax check
"""
from __future__ import annotations

from os import PathLike
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Final

from token_ import Token, Symbol, TokenType, Keyword, Loc, UnaryType


__all__ = [
	'Tokenizer',
	'TokenizerError'
]
_HARDCORE: Final[ bool ] = False


@dataclass
class TokenizerError(Exception):
	message: Optional[str] = None


class Tokenizer:
	""" Parses a string of code into a list of tokens """
	lines: list[ str ]
	code: list[ Token ]
	lineN: int = 0
	char: int = 0
	num: str = ''
	file: str
	line: str

	def __init__( self, codeString: str, file: str ) -> None:
		"""
		:param codeString: code string
		:param file: original file
		"""
		self.lines = codeString.splitlines( True )
		self.file = file
		self.code = []

	def tokenize( self ) -> Tokenizer:

		# execute until there are no more lines
		while self.lineN < len( self.lines ):
			self.line = self.lines[ self.lineN ]

			# simple keywords
			if self._getIsWord( Keyword.DECLARE ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.DECLARE, Loc.create( self, Keyword.DECLARE ) ) ]
			elif self._getIsWord( Keyword.GIVE ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.GIVE, Loc.create( self, Keyword.GIVE ) ) ]
			elif self._getIsWord( Keyword.EXPORT ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.EXPORT, Loc.create( self, Keyword.EXPORT ) ) ]
			elif self._getIsWord( Keyword.CHECK ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.CHECK, Loc.create( self, Keyword.CHECK ) ) ]
			elif self._getIsWord( Keyword.OWN ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.OWN, Loc.create( self, Keyword.OWN ) ) ]
			elif self._getIsWord( Keyword.CALL ):
				self.code += [ Token( TokenType.KEYWORD, Keyword.CALL, Loc.create( self, Keyword.CALL ) ) ]
			elif self._getIsWord( Symbol.DOT ):
				self.code += [ Token( TokenType.SYMBOL, Symbol.DOT, Loc.create( self, Symbol.DOT ) ) ]
			elif self._getIsWord( Symbol.ADD ):
				self.code += [ Token( TokenType.UNARY, UnaryType.ADD, Loc.create( self, Symbol.ADD ) ) ]
			elif self._getIsWord( Symbol.SUB ):
				self.code += [ Token( TokenType.UNARY, UnaryType.SUBTRACT, Loc.create( self, Symbol.SUB ) ) ]
			elif self._getIsWord( Symbol.DIV ):
				self.code += [ Token( TokenType.UNARY, UnaryType.DIVIDE, Loc.create( self, Symbol.DIV ) ) ]
			elif self._getIsWord( Symbol.MODULO ):
				self.code += [ Token( TokenType.UNARY, UnaryType.MODULO, Loc.create( self, Symbol.MODULO ) ) ]
			elif self._getIsWord( Symbol.GREATER ):
				self.code += [ Token( TokenType.UNARY, UnaryType.GREATER, Loc.create( self, Symbol.GREATER ) ) ]
			# keywords with prefix needed
			elif self._getIsWord( Keyword.CONSTANT ):
				loc = Loc.create( self, Keyword.VARIABLE )
				self._assertIsKw( Keyword.DECLARE, Keyword.CONSTANT, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.CONSTANT, loc ) ]
			elif self._getIsWord( Keyword.VARIABLE ):
				loc = Loc.create( self, Keyword.VARIABLE )
				self._assertIsKw( Keyword.DECLARE, Keyword.VARIABLE, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.VARIABLE, loc ) ]
			elif self._getIsWord( Keyword.BACK ):
				loc = Loc.create( self, Keyword.BACK )
				self._assertIsKw( Keyword.GIVE, Keyword.BACK, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.BACK, loc ) ]
			elif self._getIsWord( Keyword.TEMPLATE ):
				loc = Loc.create( self, Keyword.TEMPLATE )
				self._assertIsKw( Keyword.DECLARE, Keyword.TEMPLATE, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.TEMPLATE, loc ) ]
			elif self._getIsWord( Keyword.BUILD ):
				loc = Loc.create( self, Keyword.BUILD )
				self._assertIsKw( Keyword.CALL, Keyword.BUILD, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.BUILD, loc ) ]
			elif self._getIsWord( Keyword.INITIALIZER ):
				loc = Loc.create( self, Keyword.INITIALIZER )
				self._assertIsKw( Keyword.DECLARE, Keyword.INITIALIZER, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.INITIALIZER, loc ) ]
			elif self._getIsWord( Keyword.DEINITIALIZER ):
				loc = Loc.create( self, Keyword.DECLARE )
				self._assertIsKw( Keyword.DECLARE, Keyword.DECLARE, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.DEINITIALIZER, loc ) ]
			elif self._getIsWord( Keyword.IF ):
				loc = Loc.create( self, Keyword.IF )
				self._assertIsKw( Keyword.CHECK, Keyword.IF, loc )
				self.code += [ Token( TokenType.KEYWORD, Keyword.IF, loc ) ]
			elif self._getIsWord( Symbol.ARROW ):
				loc = Loc.create( self, Symbol.ARROW )
				self._assertIsKw( Symbol.RBRACE, Symbol.ARROW, loc )
				self.code += [ Token( TokenType.SYMBOL, Symbol.ARROW, loc ) ]
			elif self._getIsWord( Symbol.EQUAL ):
				if self._getIsWord('<'):
					self.code += [
						Token( TokenType.UNARY, UnaryType.GREATER_EQUAL, Loc.create( self, Symbol.EQUAL ) )
					]
				else:
					loc = Loc.create( self, Symbol.EQUAL )
					if self.code[-1].typ != TokenType.NAME:
						self._fatal( f'Missing NAME before = symbol at {loc}' )
					self.code += [ Token( TokenType.SYMBOL, Symbol.EQUAL, loc ) ]
			elif self._getIsWord( Keyword.IS ):
				loc = Loc.create( self, Keyword.IS )
				if self.code[-1].typ != TokenType.NAME:
					self._fatal( f'Missing NAME before IS keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.IS, loc ) ]
			# parens
			elif self._getIsWord(Symbol.LBRACK):
				self.code += [ Token( TokenType.SYMBOL, Symbol.LBRACK, Loc.create( self, Symbol.LBRACK ) ) ]
			elif self._getIsWord(Symbol.RBRACK):
				self.code += [ Token( TokenType.SYMBOL, Symbol.RBRACK, Loc.create( self, Symbol.RBRACK ) ) ]
			elif self._getIsWord(Symbol.LBRACE):
				self.code += [ Token( TokenType.SYMBOL, Symbol.LBRACE, Loc.create( self, Symbol.LBRACE ) ) ]
			elif self._getIsWord(Symbol.RBRACE):
				self.code += [ Token( TokenType.SYMBOL, Symbol.RBRACE, Loc.create( self, Symbol.RBRACE ) ) ]
			elif self._getIsWord(Symbol.LPAREN):
				self.code += [ Token( TokenType.SYMBOL, Symbol.LPAREN, Loc.create( self, Symbol.LPAREN ) ) ]
			elif self._getIsWord(Symbol.RPAREN):
				self.code += [ Token( TokenType.SYMBOL, Symbol.RPAREN, Loc.create( self, Symbol.RPAREN ) ) ]
			elif self._getIsWord(Symbol.SLASH):
				self.code += [ Token( TokenType.SYMBOL, Symbol.SLASH, Loc.create( self, Symbol.SLASH ) ) ]

			# special keywords
			elif self._getIsWord( Keyword.ELSE ):
				loc = Loc.create( self, Keyword.ELSE )
				if self.code[-1].value != Symbol.RBRACK:
					self._fatal( f'Missing RBRACK symbol before LS keyword at {loc}' )
				if self._peekWord() != Keyword.DO.value:
					self._fatal( f'Missing DO symbol after LS keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.ELSE, loc ) ]
			elif self._getIsWord( Keyword.SUBROUTINE ):
				loc = Loc.create( self, Keyword.SUBROUTINE )
				if len( self.code ) == 0 or self.code[-1].value not in ( Keyword.DECLARE, Keyword.CALL ):
					self._fatal( f'Missing DECLARE or CALL keyword before SUBROUTINE keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.SUBROUTINE, loc ) ]
			elif self._getIsWord( Keyword.WHEN ):
				loc = Loc.create( self, Keyword.WHEN )
				if self.code[-1].value != Keyword.UNTIL:
					self._fatal( f'Missing UNTIL keyword before WHEN keyword at {loc}' )
				if self._peekIgnoreSpaces() != Symbol.LBRACE.value:
					self._fatal( f'Missing LBRACE symbol after WHEN keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.WHEN, loc ) ]
			elif self._getIsWord( Keyword.UNTIL ):
				loc = Loc.create( self, Keyword.UNTIL )
				# ] UNTIL WHN {  }
				if self.code[-1].value == Symbol.RBRACK:
					if self._peekWord() != 'WHN':
						self._fatal( f'Missing WHN keyword after UNTIL keyword at {loc}' )
				# CHCK UNTIL {} DO [
				elif self.code[-1].value == Keyword.CHECK:
					if self._peekIgnoreSpaces() != Symbol.LBRACE.value:
						self._fatal( f'Missing LBRACE symbol after UNTIL keyword at {loc}' )
				else:
					self._fatal( f'Missing RBRACK symbol or CHECK keyword before UNTIL keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.UNTIL, loc ) ]
			elif self._getIsWord( Keyword.DO ):
				loc = Loc.create( self, Keyword.DO )
				if self._peekIgnoreSpaces() != Symbol.LBRACK.value:
					self._fatal( f'Missing LBRACK symbol after DO keyword at {loc}' )
				self.code += [ Token( TokenType.KEYWORD, Keyword.DO, loc ) ]
			elif self._peek(0) == '!':
				self._getChar()
				if self._getIsWord('IS'):
					self.code += [ Token( TokenType.UNARY, UnaryType.BANG_IS, Loc.create( self, '!IS' ) ) ]
				else:
					self.code += [ Token( TokenType.UNARY, UnaryType.BANG, Loc.create( self, '!' ) ) ]
			elif self._getIsWord( Keyword.FROM ):
				loc = Loc.create( self, Keyword.FROM )
				offset = -1
				OWN_OR_DOT, NAME = 0, 1
				expect: int = NAME
				# OWN name. name FROM something/
				while True:
					match self.code[offset]:
						case Token( value=Keyword.OWN ) as found:
							if expect == NAME:
								self._fatal(
									f'Expected NAMEs between OWN and FROM found nothing',
									found.loc.line,
									found.loc.char
								)
							break
						case Token( typ=TokenType.NAME ) as found:
							if expect == OWN_OR_DOT:
								self._fatal(
									f'Expected DOT symbol or OWN keyword before NAME found NAME',
									found.loc.line,
									found.loc.char
								)
							expect = OWN_OR_DOT
						case Token( value=Symbol.DOT ) as found:
							if expect == NAME:
								self._fatal(
									f'Expected NAMEs between OWN and FROM found nothing',
									found.loc.line,
									found.loc.char
								)
							expect = NAME
						case found:
							self._fatal(
								f'Invalid token found in import statement, expected NAME or OWN found {self.code[offset].typ} at {self.code[offset].loc}',
								found.loc.line,
								found.loc.char
							)
					offset -= 1
				self.code += [ Token( TokenType.KEYWORD, Keyword.FROM, loc ) ]
				del offset, OWN_OR_DOT, NAME, expect
			elif self._getIsWord( '|*' ):
				startLine: int = self.lineN
				found = False
				chIndex = 0
				while self.lineN < len( self.lines ) and not found:
					chLine = self.lines[ self.lineN ]
					chIndex = 0
					while chIndex < len( chLine ):
						if chLine[ chIndex ] == '*' and chLine[ chIndex + 1 ] == '|':
							found = True
							break
						chIndex += 1
					if not found:
						self.lineN += 1
				else:
					if not found:
						self._fatal(
							'Reached end of file, expected "*|" after comment at line {line}',
							startLine,
							chIndex + 1
						)
				if startLine == self.lineN:
					self._fatal(
						'Comments must be at least 2 lines long. line {line}',
						startLine,
						chIndex + 1
					)
				self.lineN += 1
				self.char = 0
				del startLine, found, chIndex, chLine
			elif self._getIsWord( '*' ):
				string: str = ''
				while True:
					if self._peek( 0 ) == '*' and string[-1] != '\\':
						break
					if self._peek( 0 ) == '*':
						string = string[: -1 ] + self._getChar()
					if self._peek( 0 ) == '\n':
						self._fatal( 'Reached end of line ({line}) without closing string character "*"' )
					string += self._getChar()
				if 'e' in string and self.code[ -4 ].value != Keyword.CONSTANT:
					self._fatal(
						'Found "e" character in non-constant string! THIS IS THE WORST POSSIBLE THING EVER!',
						col=( self.char - len(string) ) + string.find( 'e' ) + 1
					)
				if 'E' in string and self.code[ -4 ].value != Keyword.CONSTANT:
					self._fatal(
						'Found "E" character in non-constant string! THIS IS THE WORST POSSIBLE THING EVER!',
						col=( self.char - len(string) ) + string.find( 'E' ) + 1
					)
				self.char += 1
				self.code += [ Token( TokenType.STR, string, Loc.create( self, string ) ) ]
				del string
			# special stuff
			elif self._getIsWord( ' ' ):
				pass
			elif self._getIsWord( '\t' ):
				self._fatal( f'Found invalid character at {Loc.create(self, " ")} ( TAB cannot be used )' )
			elif self._getIsWord( '\n' ) or self.char == len( self.line ) - 1:
				if (
					self.code[ -1 ].typ not in ( TokenType.KEYWORD, TokenType.SYMBOL ) or
					self.code[ -1 ].value not in ( Symbol.SLASH, Symbol.LBRACK, Symbol.RBRACK, Symbol.LBRACE )
				) and len( self.line ) != 2:
					self._fatal(
						f'Missing "/" before newline at line {self.lineN} column {self.char}',
						self.lineN,
						self.char
					)
				self.lineN += 1
				self.char = 0
				if _HARDCORE:
					spaceCount: int = 0
					while self._peek( 1 + spaceCount ) == ' ':
						spaceCount += 1
					if spaceCount != 0 and spaceCount % 5 != 0:
						self._fatal( f'Indentation should be a multiple of 5 ( found {spaceCount} spaces )' )
					del spaceCount
			elif self._getIsWord( '\0' ) or ( self.char == len( self.line ) and self.lineN == len( self.lines ) - 1 ):
				break
			elif self._peek( 0 ) in ',1234567890' and self._peek() in '0123456789':
				num = ''
				while self._peek( 0 ) in ',1234567890':
					if ( numChar := self._getChar() ) != '\0':
						num += numChar
					else:
						self._fatal(
							'Reached end of line without ending /',
							self.lineN,
							self.char + len( num )
						)
				fnum = float( num.replace( ',', '.' ) )
				self.code += [ Token( TokenType.FLOAT, fnum, Loc.create( self, str( fnum ) ) ) ]
				del fnum, num, numChar
			elif self._getIsWord( ',' ):
				self.code += [
					Token( TokenType.SYMBOL, Symbol.COMMA, Loc.create( self, Symbol.COMMA ) )
				]
			else:
				name: str = ''
				while self._peek( 0 ) not in ( ' ', '\n', '{', '(', '[', ']', ')', '}', '.', '\0', '/' ):
					name += self._getChar()
				if 'e' in name.lower() and ( self.code[ -1 ].typ != TokenType.KEYWORD or self.code[ -1 ].value != Keyword.FROM ):
					self._fatal(
						'the name at line {line} and column {char} contains "e"',
						self.lineN,
						self.char - ( len( name ) - 1 ) + name.lower().index( 'e' )
					)
				self.code += [ Token( TokenType.NAME, name, Loc.create( self, name ) ) ]
				del name

		return self

	def getTokens( self ) -> list[Token]:
		return self.code

	@classmethod
	def fromFile( cls, filepath: PathLike ) -> Tokenizer:
		return cls( Path( filepath ).read_text(), str( filepath ) )

	# PRIVATE METHODS

	def _getChar( self ) -> str:
		""" Returns and consume a char """
		if self.char + 1 < len( self.line ):
			self.char = self.char + 1
			return self.line[ self.char - 1 ]
		else:
			return '\0'

	def _peek( self, offset: int = 1 ) -> str:
		""" Returns a char """
		return self.line[ self.char + offset ] if self.char + offset < len( self.line ) else '\0'

	def _peekIgnoreSpaces( self, offset: int = 1 ) -> str:
		""" Returns a char, ignoring spaces """
		while self._peek( offset ) == ' ':
			offset += 1
		return self.line[ self.char + offset ] if self.char + offset < len( self.line ) else '\0'

	def _peekWord( self, offset: int = 0 ) -> str:
		""" Returns a word """
		word: str = ''
		char: int = 1

		while True:
			if self._peek( char ) in ( ' ', '\n' ):
				if offset > 0:
					word = ''
					offset -= 1
				else:
					break
			else:
				word += self._peek( char )
			char += 1
		return word

	def _getIsWord( self, word: str | Enum ) -> bool:
		""" Check if the next word is the give word """
		if isinstance( word, Enum ):
			word = word.value

		if self.line[ self.char : self.char + len( word ) ] == word:
			self.char += len( word )
			return True
		return False

	def _assertIsKw( self, kw: Keyword | Symbol, curr: Keyword | Symbol, loc: Loc, offset: int = 0 ) -> None:
		"""
		Raises a fatal exception if the token at $offset is not the given keyword
		:param kw: Expected keyword
		:param curr: Current keyword that requires the check
		:param loc: Current keyword's location tuple
		:param offset: Offset to check
		:raises TokenizerError: When the token is wrong
		"""
		if len( self.code ) == 0 or self.code[ -1 + offset ].typ.name != kw.__class__.__name__.upper() or self.code[ -1 + offset ].value != kw:
			self._fatal(
				f'Missing {kw.name} keyword before {curr.name} keyword at line ' '{line} column {char}',
				loc[ 1 ],
				loc[ 2 ]
			)

	def _fatal( self, message: str, lineNum: int = None, col: int = None ) -> None:
		"""
		Raise an exception with debug information
		:param message: Message of the exception
		:param lineNum: Line where the error originated
		:param col: Column where the error originated
		"""
		lineNum, col = lineNum or self.lineN,  col or self.char
		err = f'ERROR: File "{self.file}", line {lineNum + 1} - {message.format( line=lineNum + 1, char=col )}\n'
		err += self.lines[ lineNum ].removesuffix('\n') + '\n'
		err += ( ' ' * ( col - 1 ) ) + '^ here'
		raise TokenizerError( err )


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
			Tokenizer(
				Path( argv[1] ).read_text(),
				argv[1]
			).tokenize().getTokens()
		)
	except ExitError as e:
		exitCode = e.code

	print(f'Done in {time() - start}')
	exit(exitCode)
