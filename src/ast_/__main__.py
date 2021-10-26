"""
Tries to parse the given file into an AST.
"""

from time import time
from pathlib import Path
from sys import argv

from utils import ExitError
from . import parser, astPrinter
from tokenizer import parse


start = time()
exitCode = 0
try:
	astPrinter.AstPrinter().print(
		parser.Parser(
			parse(
				Path( argv[ 1 ] ).read_text(),
				argv[ 1 ]
			)
		).parse()  # type: ignore
	)
except ExitError as e:
	exitCode = e.code

print( f'Done in {time() - start}' )
exit( exitCode )
