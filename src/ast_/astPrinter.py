"""
Given an AST, pretty prints it.
"""


from typing import cast, TextIO

from .expr import Visitor, Binary, Grouping, Literal, Unary, Expr


class AstPrinter(Visitor[str]):
	file: TextIO

	def __init__( self, file: TextIO ):
		self.file = file

	def print( self, expr: Expr ) -> None:
		print( expr.accept(self), file=self.file )

	def parenthesize( self, name: str, *args: Expr ) -> str:
		string: str = f'({name}'
		for expr in args:
			string += f' {expr.accept( self )}'
		return string + ')'

	def visitBinaryExpr( self, binary: Binary ) -> str:
		return self.parenthesize( cast( str, binary.operator.value ), binary.left, binary.right )

	def visitGroupingExpr( self, grouping: Grouping ) -> str:
		return self.parenthesize( 'group', grouping.expression )

	def visitLiteralExpr( self, literal: Literal ) -> str:
		if literal.value is None:
			return "NOTHING"
		return str( literal.value )

	def visitUnaryExpr( self, unary: Unary ) -> str:
		return self.parenthesize( cast( str, unary.operator.value ), unary.right )


if __name__ == '__main__':
	from tokenizer import Token, TokenType, UnaryType

	AstPrinter().print(
		Binary(
			Unary(
				Token(TokenType.UNARY, '', ('', 0, 0), UnaryType.SUBTRACT ),
				Literal(123)
			),
			Token(TokenType.UNARY, '', ('', 0, 0), UnaryType.ADD),
			Grouping( Literal(45.67) )
		)
	)
