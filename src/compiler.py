import os
import sys
from json import loads
from pathlib import Path
from argparse import ArgumentParser
from typing import Literal, cast, TextIO
from time import time
from importlib import import_module

from backend import Backend, BACKENDS
import ast_.parser
import tokenizer

parser = ArgumentParser(
	prog='compiler.py' if getattr(sys, 'frozen', False) else 'endcc',
	description='End C Compiler'
)
parser.add_argument(
	'-f',
	'--file',
	help='Input file',
	action='store',
	type=Path,
	dest='file'
)
parser.add_argument(
	'-b',
	'--backend',
	help='Must be one of "inter", "llvm", "wasm", "py", "jvm", "neko" or "js"',
	action='store',
	type=str,
	dest='backend'
)
parser.add_argument(
	'-c',
	'--config',
	help='Sets the config file to the provided path',
	action='store',
	type=Path,
	default='.endcc.json',
	dest='configFile'
)
parser.add_argument(
	'-a',
	'--aftercomp',
	help='Sets the python script exececuted after compile to the provided file',
	action='store',
	type=Path,
	dest='postCompileScript'
)
parser.add_argument(
	'-v',
	'--verbosity',
	help='Sets the verbosity of the log (0: everything 1: warns+errors 2: errors)',
	action='store',
	type=int,
	dest='verboseLevel'
)
parser.add_argument(
	'--backend-info',
	help='Used to get information about available backends',
	action='store_true',
	default=False,
	dest='showBackendHelp'
)
parser.add_argument(
	'--interactive',
	help='Used to run the interpreter in interactive mode',
	action='store_true',
	default=False,
	dest='interactiveMode'
)


class Arguments:
	file: Path
	backend: Literal['inter', 'llvm', 'wasm', 'py', 'jvm', 'neko', 'js']
	showBackendHelp: bool
	configFile: Path
	postCompileScript: Path
	interactiveMode: bool
	# 0: everything 1: warns up 2: only errors
	verboseLevel: int


def main() -> int:
	# cli arguments
	args: Arguments = cast( Arguments, parser.parse_args( sys.argv[ 1: ] ) )
	# backend help (--backed-info)
	if args.showBackendHelp:
		txt = 'note: backends with * are not yet available\n'
		txt += 'Supported backends:\n'
		for backendKey, backend in BACKENDS.items():
			txt += f' - {backend.name} ({backendKey}){"" if backend.available else "*"}\n'
			txt += f'\t{backend.help}\n'
		print(txt)
		exit(0)

	# config file defaults
	cfgFile = Path(args.configFile)
	if cfgFile.exists():
		print( f'[INFO] Using config at {cfgFile}' )
		cfg: dict = loads( cfgFile.read_text() )
		args.file = args.file or Path( cfg['defaultFile'] )
		args.backend = args.backend or cfg.get('defaultBackend', 'inter')
		args.verboseLevel = cfg.get( 'verboseLevel', args.verboseLevel )
		args.postCompileScript = (
			args.postCompileScript or
			Path( cfg.get('postCompileScript') ) if cfg.get('postCompileScript') else None
		)

	def log(verb: int, msg: str, file: TextIO = sys.stdout) -> None:
		if args.verboseLevel <= verb:
			print(msg, file=file)

	exitCode: int = 0
	# execute build
	try:
		# interactive mode
		if args.interactiveMode:
			return import_module( 'backend.interpreter.interactive' ).interactiveMain()

		if not args.file.exists():
			log(2, f'[ERROR] File {args.file} not found.', sys.stderr)
			return 1
		log(0, f'[INFO] Compiling {args.file}')

		log(0, f'[INFO] Tokenizing..')
		tokens = tokenizer.parse( args.file.read_text(), str( args.file ) )

		log(0, f'[INFO] Generating AST..')
		ast = ast_.parser.Parser( tokens ).parse()

		log(0, f'[INFO] Selecting backend..')
		if args.backend not in BACKENDS:
			log( 2, f'[ERROR] Trying to use invalid backend ({args.backend}), aborting.', sys.stderr )
			return 1
		backend = BACKENDS[args.backend]
		if not backend.available:
			log(2, f'[ERROR] Selected backend ({backend.name}) is not available, aborting.', sys.stderr)
			return 1

		log(0, f'[INFO] Executing backend "{backend.name}"..')
		exitCode = cast( Backend, import_module( backend.pkg ) ).backendMain(ast)

		if args.postCompileScript:
			if not args.postCompileScript.exists():
				log(1, f'[WARN] Post compile script "{args.postCompileScript}" does not exist.')
			else:
				log(0, f'[INFO] Executing post compile script "{args.postCompileScript}"..')
				os.system( f'{sys.executable} {args.postCompileScript} {args.file.absolute()} {args.backend}' )

	except SystemExit as e:
		return e.code
	return exitCode


if __name__ == '__main__':
	start = time()
	_exitCode = main()
	print( f'Done in {time() - start}' )
	exit( _exitCode )
