from pathlib import Path
from sys import argv, stderr
from argparse import ArgumentParser

import ast_
import tokenizer

parser = ArgumentParser(
	prog='compiler.py',
	description='End C compiler'
)
parser.add_argument(
	'file',
	help='input file',
	action='store',
	type=Path
)


class Arguments:
	file: Path


def main():
	from typing import cast
	from time import time
	start = time()
	exitCode = 0
	args: Arguments = cast( Arguments, parser.parse_args( argv[ 1: ] ) )
	try:
		if not args.file.exists():
			print(f'[ERROR] File {args.file} not found.', file=stderr)
			exit(1)
		print(f'[INFO] Compiling {args.file}')
		print(f'[INFO] Tokenizing..')
		tokens = tokenizer.parse( args.file.read_text(), str( args.file ) )
		print(f'[INFO] Generating AST..')
		ast = astgen.genAst( tokens, str( args.file ) )
	except SystemExit as e:
		exitCode = e.code
	print( f'Done in {time() - start}' )
	exit(exitCode)



if __name__ == '__main__':
	main()
