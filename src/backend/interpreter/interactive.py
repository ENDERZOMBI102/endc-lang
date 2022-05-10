"""
Interactive intepreter implementation.
"""

from sys import stderr

import ast_.parser
import token_.tokenizer
from cli import args
from log import error
from . import Interpreter, InterpreterError, errorHandler


def interactiveMain() -> int:
	interpreter = Interpreter()
	while True:
		inp: str
		try:
			inp = input('>>> ')
		except EOFError:
			return 0
		# as we're in the interactive interpreter, we can be a little more forgiving
		if not inp.endswith('/'):
			inp += '/'
		# is it a exit call?
		if inp.startswith('CALL xit{'):
			if inp.endswith('}/'):
				# parse exit code
				exitCode = inp.removeprefix('CALL xit{').removesuffix('}/')
				if exitCode == '':
					exitCode = '0'
				if exitCode.isdigit():
					return int(exitCode)
				else:
					print( 'function xit takes an InTgR or VoId', file=stderr )
			else:
				print( 'missing / at end of input', file=stderr )
		else:
			# its not, interpret it
			try:
				tokens = token_.tokenizer.Tokenizer( inp, '<stdin>' ).tokenize().getTokens()
				ast = ast_.parser.Parser( tokens ).parse()
				if ( val := interpreter.interpret( ast ) ) is not None:
					print( val )
			except token_.tokenizer.TokenizerError as e:
				error( f'Failed to tokenize expression: {e.args[0]}' )
			except ast_.parser.ParseError as e:
				error( f'Failed to parse expression: "{e.args[0]}"' )
			except InterpreterError as e:
				error( f'Interpreter error: {e.args[0]}: {e.args[1]}' )
			except Exception as e:
				error( f'Implementation error: {errorHandler.getTracebackText(e)}' )
				if args.exitOnImplementationError:
					return -1
