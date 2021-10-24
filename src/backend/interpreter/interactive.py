from sys import stderr

import ast_.parser
import tokenizer
from . import Interpreter, InterpreterError


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
				print(
					intpr.evaluate(
						ast_.parser.Parser(
							tokenizer.parse(
								inp,
								'<stdin>'
							)
						).parse()
					)
				)
			except tokenizer.TokenizerError as e:
				print(f'Failed to tokenize expression: {e.args[0]}', file=stderr)
			except ast_.parser.ParseError as e:
				print(f'Failed to parse expression: "{e.args[0]}"', file=stderr)
			except InterpreterError as e:
				print(f'{e.args[0]}: {e.args[1]}', file=stderr)
