from sys import stderr

import ast_.parser
import tokenizer
from . import Interpreter


def interactiveMain() -> int:
	intpr = Interpreter()
	while True:
		inp = input('>>> ')
		if inp.startswith('CALL xit{'):
			exitCode = inp.removeprefix('CALL xit{').removesuffix('}/')
			if exitCode == '':
				exitCode = '0'
			if exitCode.isdigit():
				return int(exitCode)
			else:
				print( 'function xit takes an InTgR or VoId', file=stderr )
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
			except SystemExit:
				print(f'Failed to parse expression: "{inp}"')
