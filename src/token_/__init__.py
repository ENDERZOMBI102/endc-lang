"""
Transforms a string into a stream/list of tokens, while performing a basic syntax check
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, TYPE_CHECKING


if TYPE_CHECKING:
	from token_.tokenizer import Tokenizer


class Loc( NamedTuple ):
	file: str
	line: int
	char: int

	@classmethod
	def create( cls, tokenizer: 'Tokenizer', kw: str | Keyword | Symbol ) -> Loc:
		return cls(
			tokenizer.file,
			tokenizer.lineN,
			tokenizer.char - ( len( kw.value if isinstance( kw, Enum ) else kw ) - 1 )
		)

	def __str__( self ) -> str:
		return f'line {self.line} char {self.char} in file {self.file}'


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
	LBRACK = '['
	RBRACK = ']'
	LBRACE = '{'
	RBRACE = '}'
	SLASH = '/'
	COLON = ':'
	COMMA = ','
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
	SUBTRACT = auto()		# +
	ADD = auto()  			# -
	DIVIDE = auto()			# ;
	MODULO = auto()			# \
	BANG = auto()			# !
	GREATER = auto()		# <
	GREATER_EQUAL = auto()  # =<
	BANG_IS = auto()		# !IS


class TokenType(Enum):
	NAME = auto()
	FLOAT = auto()
	STR = auto()
	COMMENT = auto()
	KEYWORD = auto()
	SYMBOL = auto()
	UNARY = auto()
	EOF = auto()


@dataclass
class Token:
	typ: TokenType
	value: float | str | Keyword | Symbol | UnaryType
	loc: Loc