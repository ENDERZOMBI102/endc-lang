from unittest import main, TestCase
import sys


sys.path.append('src')


class ExpressionTest(TestCase):
	def testImports( self ) -> None:
		import tokenizer
		import ast_.parser

	def testTokenizerWithBadCode( self ) -> None:
		from tokenizer import TokenizerError, parse
		with self.assertRaises(TokenizerError):
			parse( '|* comment test *|', '<test>' )


if __name__ == '__main__':
	main()
