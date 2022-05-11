"""
Parsers a stream/list of tokens into an abstract binary tree, while doing an intermediate syntax check
"""

from typing import Final, Union, Optional

from ast_ import ParseError
from ast_.expr import Expr, Binary, Unary, Literal, Grouping
from cli import Arguments
from token_ import Token, Keyword, TokenType, UnaryType, Loc, Symbol


Error = tuple[int, str, str]
config: Arguments


class Parser:
	errors: list[Error]
	tokens: Final[ list[Token] ]
	current: int = 0

	def __init__(self, tokens: list[Token]) -> None:
		self.tokens = tokens + [ Token(TokenType.EOF, '', Loc('', 0, 0) ) ]
		self.errors = []

	def parse( self ) -> Optional[Expr]:
		self.errors.clear()
		val = self.expression()
		if isinstance( val, ParseError ):
			raise ParseError( self.errors, val )
		return val

	def expression( self ) -> Expr:
		return self.equality()

	def equality( self ) -> Expr:
		expr: Expr = self.comparison()

		while self.match(Keyword.IS):
			operator: Token = self.previous()
			right: Expr = self.comparison()
			expr = Binary(expr, operator, right)

		return expr

	def comparison( self ) -> Expr:
		expr: Expr = self.term()

		while self.match(UnaryType.GREATER, UnaryType.GREATER_EQUAL):
			operator: Token = self.previous()
			right: Expr = self.term()
			expr = Binary(expr, operator, right)

		return expr

	def term( self ) -> Expr:
		expr: Expr = self.factor()

		while self.match(UnaryType.SUBTRACT, UnaryType.ADD):
			operator: Token = self.previous()
			right: Expr = self.factor()
			expr = Binary(expr, operator, right)

		return expr

	def factor( self ) -> Expr:
		expr: Expr = self.unary()

		while self.match(UnaryType.DIVIDE, UnaryType.MODULO):
			operator: Token = self.previous()
			right: Expr = self.unary()
			expr = Binary( expr, operator, right )

		return expr

	def unary( self ) -> Expr:
		if self.match(UnaryType.BANG, UnaryType.SUBTRACT):
			operator: Token = self.previous()
			right: Expr = self.unary()
			return Unary(operator, right)
		return self.primary()

	def primary( self ) -> Expr:
		if self.match(Keyword.FALSE):
			return Literal(False)
		if self.match(Keyword.NOTHING):
			return Literal(None)

		if self.matchType(TokenType.FLOAT, TokenType.STR):
			return Literal(self.previous().value)

		if self.match(Symbol.LBRACE):
			expr: Expr = self.expression()
			self.consume(Symbol.RBRACE, 'Expect } after expression.')
			return Grouping(expr)

		raise self.error( self.peek(), 'Expect expression.' )

	def consume( self, typ: TokenType | Keyword | UnaryType | Symbol, message: str ) -> Token:
		if isinstance(typ, TokenType):
			if self.checkType(typ):
				return self.advance()
		else:
			if self.check(typ):
				return self.advance()

		raise self.error( self.peek(), message )

	def error( self, token: Token, message: str ) -> ParseError:
		self.errors.append(
			(
				token.loc[1],
				'at end' if token.typ == TokenType.EOF else f"at '{token.value}'",
				message
			)
		)
		return ParseError( self.errors[-1] )

	def hadErrors( self ) -> bool:
		return len( self.errors ) != 0

	def synchronize( self ) -> None:
		self.advance()  # DCLAR SUBROUTIN func{} [ CALL PRINTTO{ STDOUT. *Hllo world!* }/ ]

		while not self.isAtEnd():
			if self.previous().value == Symbol.SLASH:
				return

			if self.peek().value in (
					Keyword.DECLARE,
					Keyword.EXPORT,
					Keyword.CHECK,
					Keyword.CALL,
					Keyword.GIVE,
					Keyword.UNTIL,
			):
				return

			self.advance()

	def match( self, *types: Keyword | UnaryType | Symbol ) -> bool:
		for typ in types:
			if self.check(typ):
				self.advance()
				return True
		return False

	def matchType( self, *types: TokenType ) -> bool:
		for typ in types:
			if self.checkType(typ):
				self.advance()
				return True
		return False

	def check( self, typ: Union[Keyword, UnaryType] ) -> bool:
		if self.isAtEnd():
			return False
		return self.peek().value == typ

	def checkType( self, typ: TokenType ) -> bool:
		if self.isAtEnd():
			return False
		return self.peek().typ == typ

	def advance( self ) -> Token:
		if not self.isAtEnd():
			self.current += 1
		return self.previous()

	def isAtEnd( self ) -> bool:
		return self.peek().typ == TokenType.EOF

	def peek( self ) -> Token:
		return self.tokens[self.current]

	def previous( self ) -> Token:
		return self.tokens[self.current - 1]
