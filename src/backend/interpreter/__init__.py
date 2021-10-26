from typing import Any, cast

from ast_.expr import Visitor, Binary, Grouping, Literal, Unary, Expr
from backend.interpreter import errorHandler
from tokenizer import UnaryType
from utils import ExitError


class InterpreterError(RuntimeError):
	pass


# noinspection PyMethodMayBeStatic
class Interpreter(Visitor[object]):

	def visitBinaryExpr( self, binary: Binary ) -> object:
		left: Any = self.evaluate(binary.left)
		right: Any = self.evaluate(binary.right)

		op: UnaryType = cast( UnaryType, binary.operator.value )

		# math
		if op is UnaryType.SUBTRACT:
			self.checkNumberOperand(op, right)
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
		return self.evaluate( grouping.expression )

	def visitLiteralExpr( self, literal: Literal ) -> object:
		return literal.value

	def visitUnaryExpr( self, unary: Unary ) -> object:
		right: Any = self.evaluate( unary.right )

		if unary.operator.value == UnaryType.SUBTRACT:
			return -float(right)
		if unary.operator.value == UnaryType.BANG:
			return not self.isTruthy(right)

		# Unreachable
		return None

	def evaluate( self, expr: Expr ) -> object:
		if isinstance(expr, Expr):
			return expr.accept(self)
		return expr

	# helper methods

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

	def checkNumberOperand( self, op: UnaryType, right: Any ) -> None:
		if isinstance(right, float):
			return
		raise InterpreterError(op, 'Operand must be a number')

	def stringify( self, obj: Any ) -> str:
		if obj is None:
			return 'NOTHING'
		elif isinstance( obj, float ):
			txt: str = str(obj)
			if txt.endswith('.0'):
				return txt[:-2]
		elif isinstance( obj, str ):
			return f'*{obj}*'

		return str(obj)

	def interpret( self, expr: Expr ) -> None:
		try:
			obj = self.evaluate( expr )
			print( self.stringify(obj) )
		except InterpreterError as e:
			raise ExitError(
				-1,
				f'Implementation error: {errorHandler.getTracebackText(e)}'
			)


def backendMain(ast: Expr) -> int:
	try:
		Interpreter().evaluate(ast)
	except InterpreterError as e:
		print(e)
		return 1
	return 0

