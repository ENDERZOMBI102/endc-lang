from argparse import ArgumentParser
from pathlib import Path
from sys import argv
from typing import Any


class PythonWriter:
	file: Path
	_lazy: bool
	_content: str = ''
	_indentLevel: int = 0

	def __init__(self, file: Path, lazy: bool = True) -> None:
		self.file = file
		self._lazy = lazy

	def __enter__(self) -> None:
		self._indentLevel += 1

	def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
		self._indentLevel -= 1

	def __del__(self) -> None:
		if self._lazy:
			self.file.write_text(self._content)

	def write( self, text: str, end: str = '\n' ) -> None:
		text = ( '\t' * self._indentLevel ) + text + end
		self._content += text
		if not self._lazy:
			with self.file.open('at') as file:
				file.write(text)
	
	def dup( self ) -> None:
		self.write('\n')


def defineType( writer: PythonWriter, baseName: str, className: str, fields: list[str] ) -> None:
	writer.write(f'@dataclass')
	writer.write(f'class {className}({baseName}):')
	with writer:
		for field in fields:
			writer.write( ': '.join( field.split()[::-1] ) )
		writer.write('')
		writer.write('def accept( self, visitor: Visitor[R] ) -> R:')
		with writer:
			writer.write(f'return visitor.visit{className}{baseName}(self)')


def defineVisitor( writer: PythonWriter, baseName: str, types: list[str] ) -> None:
	writer.write('class Visitor(Generic[R], metaclass=ABCMeta):')
	with writer:
		for typ in types:
			typeName: str = typ.split( ':' )[ 0 ].strip()
			writer.write('')
			writer.write('@abstractmethod')
			writer.write( f'def visit{typeName}{baseName}( self, {typeName.lower()}: \'{typeName}\' ) -> R:' )
			with writer:
				writer.write('pass')


def defineAst( outputDir: Path, baseName: str, types: list[str] ) -> None:
	path = outputDir / ( baseName.lower() + '.py' )
	writer = PythonWriter( path )

	# init
	writer.write('from abc import ABCMeta, abstractmethod')
	writer.write('from typing import TypeVar, Generic')
	writer.write('from dataclasses import dataclass')
	writer.write('')
	writer.write('from tokenizer import Token')
	writer.dup()
	writer.write('R = TypeVar("R")')
	writer.write('Object = object')
	writer.dup()
	# visitor class
	defineVisitor( writer, baseName, types )
	writer.dup()
	# base class
	writer.write(f'class {baseName}(metaclass=ABCMeta):')
	with writer:
		writer.write('@abstractmethod')
		writer.write('def accept(self, visitor: Visitor[R]) -> R:')
		with writer:
			writer.write('pass')
	# types
	for typ in types:
		className: str = typ.split(':')[0].strip()
		fields: str = typ.split(':')[1].strip()
		writer.dup()
		defineType( writer, baseName, className, fields.split(', ') )


if __name__ == '__main__':
	parser = ArgumentParser(
		prog='AST Generator',
		description='Tool to generate the AST classes'
	)
	parser.add_argument(
		'--out',
		help='output directory',
		type=Path,
		default=Path( '.' ),
		dest='outputDir'
	)
	outputDir = parser.parse_args( argv[ 1: ] ).outputDir

	defineAst(
		outputDir,
		'Expr',
		[
			'Binary   : Expr left, Token operator, Expr right',
			'Grouping : Expr expression',
			'Literal  : Object value',
			'Unary    : Token operator, Expr right'
		]
	)
