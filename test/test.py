from pathlib import Path
from unittest import main, TestCase
import sys

sys.path.append('src')

from tokenizer import TokenizerError
import tokenizer


class ExpressionTest(TestCase):
	def testTokenizerWithBadCode( self ) -> None:
		# one line comments
		with self.assertRaises(TokenizerError):
			tokenizer.parse( '|* comment test *|', '<test>' )
		# opening curly brace without word/func
		with self.assertRaises(TokenizerError):
			tokenizer.parse( '{', '<test>' )
		# FUNC without DCLAR or CALL
		with self.assertRaises(TokenizerError):
			tokenizer.parse( 'FUNC', '<test>' )
		# unfinished string
		with self.assertRaises( TokenizerError ):
			tokenizer.parse( '*/\n', '<test>' )
		# CONSTANT without DCLAR
		with self.assertRaises( TokenizerError ):
			tokenizer.parse( 'CONSTANT', '<test>' )
		# BACK without GIV
		with self.assertRaises( TokenizerError ):
			tokenizer.parse( 'BACK', '<test>' )
		# line without /
		with self.assertRaises( TokenizerError ):
			tokenizer.parse( 'GIV BACK 0', '<test>' )

	def testTokenizerWithGoodCode( self ) -> None:
		for example in Path('examples').glob('*.endc'):
			with self.subTest():
				try:
					tokenizer.parse( example.read_text(), example.name )
				except TokenizerError as e:
					assert False, f'Failed on example "{example.name}": {e.args}'


if __name__ == '__main__':
	main()
