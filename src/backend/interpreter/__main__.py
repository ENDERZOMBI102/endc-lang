from time import time
from pathlib import Path
from pprint import pprint
from sys import argv

from ast_.parser import Parser
from backend.interpreter import Interpreter
from tokenizer import parse
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
			).parse()
		)
	)
except ExitError as e:
	exitCode = e.code

print(f'Done in {time() - start}')
exit(exitCode)
