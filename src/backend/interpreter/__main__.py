"""
Interprets a given file
"""

import sys
from time import time
from pathlib import Path
from pprint import pprint
from sys import argv

from ast_.parser import Parser
from backend.interpreter import Interpreter
from tokenizer import parse, TokenizerError
from utils import ExitError

start = time()
exitCode = 0
try:
	pprint(
		Interpreter().evaluate(
			Parser(
				parse(
					Path( argv[1] ).read_text(),
					argv[1]
				)
			).parse()  # type: ignore
		)
	)
except ExitError as e:
	exitCode = e.code
except TokenizerError as e:
	print( e.message, file=sys.stderr )
	exitCode = -1

print(f'Done in {time() - start}')
exit(exitCode)
