"""
Unit Tests for all EndC compiler modules
"""

import sys; sys.path.append('src')
from pathlib import Path
from unittest import main, TestCase

from token_ import tokenizer
from ast_ import parser
from backend import interpreter


class ExpressionTest(TestCase):
	def testTokenizerWithBadCode( self ) -> None:
		# one line comments
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( '|* comment test *|', '<test>' ).tokenize().getTokens()
		# FUNC without DCLAR or CALL
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( 'SUBROUTIN', '<test>' ).tokenize().getTokens()
		# unfinished string
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( '*/\n', '<test>' ).tokenize().getTokens()
		# CONSTANT without DCLAR
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( 'CONSTANT', '<test>' ).tokenize().getTokens()
		# BACK without GIV
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( 'BACK', '<test>' ).tokenize().getTokens()
		# line without /
		with self.assertRaises( tokenizer.TokenizerError ):
			tokenizer.Tokenizer( 'GIV BACK 0', '<test>' ).tokenize().getTokens()

	def testTokenizerWithGoodCode( self ) -> None:
		for example in Path('examples').glob('*.endc'):
			with self.subTest():
				try:
					tokenizer.Tokenizer( example.read_text(), example.name )
				except tokenizer.TokenizerError as e:
					assert False, f'Failed on example "{example.name}": {e.args}'

	def testParserWithGoodCode( self ) -> None:
		for example in Path('examples').glob('*.endc'):
			with self.subTest():
				try:
					parser.Parser(
						tokenizer.Tokenizer(
							example.read_text(),
							example.name
						).tokenize().getTokens()
					).parse()
				except parser.ParseError as e:
					assert False, f'Failed on example "{example.name}": {e.args}'

	def testInterpreterWithGoodCode( self ) -> None:
		for example in Path('examples').glob('*.endc'):
			with self.subTest(f'file {example}'):
				try:
					interpreter.Interpreter().interpret(
						parser.Parser(
							tokenizer.Tokenizer(
								example.read_text(),
								example.name
							).tokenize().getTokens()
						).parse()
					)
				except parser.ParseError as e:
					assert False, f'Failed on example "{example.name}": {e.args}'


if __name__ == '__main__':
	main()
