from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from tokenizer import Token
from typing import TypeVar, Generic


R = TypeVar("R")
Object = object


class Visitor(Generic[R], metaclass=ABCMeta):
	
	@abstractmethod
	def visitBinaryExpr(self, binary: 'Binary') -> R:
		pass
	
	@abstractmethod
	def visitGroupingExpr(self, grouping: 'Grouping') -> R:
		pass
	
	@abstractmethod
	def visitLiteralExpr(self, literal: 'Literal') -> R:
		pass
	
	@abstractmethod
	def visitUnaryExpr(self, unary: 'Unary') -> R:
		pass


class Expr(metaclass=ABCMeta):
	@abstractmethod
	def accept(self, visitor: Visitor[R]) -> R:
		pass


@dataclass
class Binary(Expr):
	def accept(self, visitor: Visitor[R]) -> R:
		return visitor.visitBinaryExpr(self)
	left: Expr
	operator: Token
	right: Expr


@dataclass
class Grouping(Expr):
	def accept(self, visitor: Visitor[R]) -> R:
		return visitor.visitGroupingExpr(self)
	expression: Expr


@dataclass
class Literal(Expr):
	def accept(self, visitor: Visitor[R]) -> R:
		return visitor.visitLiteralExpr(self)
	value: Object


@dataclass
class Unary(Expr):
	def accept(self, visitor: Visitor[R]) -> R:
		return visitor.visitUnaryExpr(self)
	operator: Token
	right: Expr
