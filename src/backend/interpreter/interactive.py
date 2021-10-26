import traceback
from sys import stderr

import ast_.parser
import tokenizer
from cli import args
from . import Interpreter, InterpreterError, errorHandler


def interactiveMain() -> int:
	intpr = Interpreter()
	while True:
		inp = input('>>> ')
		if inp.startswith('CALL xit{'):
			if inp.endswith('}/'):
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
			try:
				intpr.interpret(
					ast_.parser.Parser(
						tokenizer.parse(
							inp,
							'<stdin>'
						)
					).parse()  # type: ignore
				)
			except tokenizer.TokenizerError as e:
				print(f'Failed to tokenize expression: {e.args[0]}', file=stderr)
			except ast_.parser.ParseError as e:
				print(f'Failed to parse expression: "{e.args[0]}"', file=stderr)
			except InterpreterError as e:
				print(f'Interpreter error: {e.args[0]}: {e.args[1]}', file=stderr)
			except Exception as e:
				print(
					'Implementation error: ' + errorHandler.getTracebackText(e),
					file=stderr
				)
				import compiler
				if args.exitOnImplementationError:
					return -1
