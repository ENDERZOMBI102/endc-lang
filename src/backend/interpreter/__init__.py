from typing import Any

from ast_.expr import Visitor, Binary, Grouping, Literal, Unary, Expr
from tokenizer import UnaryType


class Interpreter(Visitor[object]):

	def visitBinaryExpr( self, binary: Binary ) -> object:
		left: Any = self.evaluate(binary.left)
		right: Any = self.evaluate(binary.right)

		op: UnaryType = binary.operator.value

		# math
		if op is UnaryType.SUBTRACT:
			return float(left) - float(right)
		elif op is UnaryType.DIVIDE:
			return float(left) / float(right)
		elif op is UnaryType.MODULO:
			return float(left) % float(right)
		elif op is UnaryType.ADD:
			if isinstance( left, str ):
				return str( left ) + str( right )
			elif isinstance(left, float):
				return float(left) + float(right)
		# comparisons
		elif op is UnaryType.GREATER:
			return float(left) > float(right)
		elif op is UnaryType.GREATER_EQUAL:
			return float(left) >= float(right)
		elif op is UnaryType.BANG_IS:
			return not self.isEqual(left, right)

		# unreachable
		return None

	def visitGroupingExpr( self, grouping: Grouping ) -> object:
		return self.evaluate( grouping )

	def visitLiteralExpr( self, literal: Literal ) -> object:
		return literal.value

	def visitUnaryExpr( self, unary: Unary ) -> object:
		right: object = self.evaluate( unary.right )

		if unary.operator.value == UnaryType.SUBTRACT:
			return -float(right)
		if unary.operator.value == UnaryType.BANG:
			return not self.isTruthy(right)

		# Unreachable
		return None

	def evaluate( self, expr: Expr ) -> object:
		return expr.accept(self)

	def isTruthy( self, obj: object ) -> bool:
		if obj is None:
			return False

		if isinstance(obj, bool):
			return obj

		return True

	def isEqual( self, left: Any, right: Any ) -> bool:
		if left is None and right is None:
			return True
		if left is None:
			return False
		return left == right


def backendMain(ast) -> bool:
	try:
		print( Interpreter().evaluate(ast) )
	except Exception as e:
		print(e)
		return False
	return True
