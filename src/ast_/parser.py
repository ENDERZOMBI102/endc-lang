"""
Parsers a stream/list of tokens into an abstract binary tree, while doing an intermediate syntax check
"""

from typing import Final, Union, Optional

from ast_ import ParseError
from ast_.expr import Expr, Binary, Unary, Literal, Grouping
from tokenizer import Token, Keyword, TokenType, UnaryType


hadError: bool = False


def report(line: int, where: str, message: str) -> None:
	global hadError
	print( f'[line {line}] Error {where}: {message}' )
	hadError = True


def error(token: Token, message: str) -> None:
	if token.typ == TokenType.EOF:
		report( token.loc[1], 'at end', message )
	else:
		report( token.loc[1], f"at '{token.value}'", message )


class Parser:
	tokens: Final[ list[Token] ]
	current: int = 0

	def __init__(self, tokens: list[Token]) -> None:
		self.tokens = tokens + [ Token(TokenType.EOF, '', ('', 0, 0), '') ]

	def parse( self ) -> Optional[Expr]:
		try:
			return self.expression()
		except ParseError:
			return None

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
		if self.match(Keyword.NO):
			return Literal(False)
		if self.match(Keyword.NOTHING):
			return Literal(None)

		if self.matchType(TokenType.FLOAT, TokenType.STR):
			return Literal(self.previous().value)

		if self.match(Keyword.CurlyOpen):
			expr: Expr = self.expression()
			self.consume(Keyword.CurlyClose, 'Expect } after expression.')
			return Grouping(expr)

		raise self.error( self.peek(), 'Expect expression.' )

	def consume( self, typ: Union[TokenType, Keyword, UnaryType], message: str ) -> Token:
		if isinstance(typ, TokenType):
			if self.checkType(typ):
				return self.advance()
		else:
			if self.check(typ):
				return self.advance()

		raise self.error( self.peek(), message )

	def error( self, token: Token, message: str ) -> ParseError:
		error( token, message )
		return ParseError()

	def syncronize( self ) -> None:
		self.advance()

		while not self.isAtEnd():
			if self.previous().value == Keyword.Slash:
				return

			if self.peek().value in (
					Keyword.DCLAR,
					Keyword.XPORT,
					Keyword.CHCK,
					Keyword.CALL,
					Keyword.GIV,
					Keyword.WHIL,
			):
				return

			self.advance()

	def match( self, *types: Union[Keyword, UnaryType] ) -> bool:
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
