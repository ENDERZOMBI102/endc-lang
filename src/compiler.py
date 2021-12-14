"""
Main file of the endc compiler.
Connects all the pieces together.

 - Uses the cli arguments to run the correct backend with valid parameters.
 - Tracks how much time the compilation process took.
"""

import os
import sys
from sys import exit
from json import loads
from pathlib import Path
from typing import cast, Union
from time import time
from importlib import import_module

from backend import BACKENDS
import ast_.parser
import tokenizer
from cli import args
from log import warn, info, error
from utils import ExitError
from platforms import Platform


def main() -> int:
	if args.execPyFile is not None:
		# just exec the py file
		sys.argv = args.execPyArgs
		exec( Path(args.execPyFile).read_text(), {}, {} )
		exit(0)

	# backend help (--backed-info)
	if args.showBackendHelp:
		txt = 'note: backends with leading * are not yet available\n'
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
		cfg: dict[ str, Union[ str, int ] ] = loads( cfgFile.read_text() )
		args.file = args.file or Path( cast( str, cfg['defaultFile'] ) )
		args.backend = args.backend or Platform.findAdeguate( cfg.get('defaultBackend', 'inter') )
		args.verboseLevel = cast( int, cfg.get( 'verboseLevel', args.verboseLevel ) )
		args.postCompileScript = (
			args.postCompileScript or
			Path( cast( str, cfg.get('postCompileScript') ) ) if cfg.get('postCompileScript') else None
		)

	exitCode: int = 0
	# execute build
	try:
		# interactive mode
		if args.interactiveMode:
			return import_module( 'backend.interpreter.interactive' ).interactiveMain()  # type: ignore

		if not args.file.exists():
			error( f'File {args.file} not found.')
			return 1
		info( f'Compiling {args.file}')

		info( f'Tokenizing..')
		tokens = tokenizer.parse( args.file.read_text(), str( args.file ) )

		info( f'Generating AST..')
		ast = ast_.parser.Parser( tokens ).parse()
		if ast is None:
			error( f'Failed to generate AST, aborting.' )
			return 1

		info( f'Selecting backend..')
		try:
			args.backend = Platform.findAdeguate( args.backend )
		except ValueError:
			error( f'Trying to use invalid backend ({args.backend}), aborting.' )
			return 1
		backend = BACKENDS[args.backend]
		if not backend.available:
			error( f'Selected backend ({backend.name}) is not available, aborting.')
			return 1

		info( f'Executing backend "{backend.name}"..')
		exitCode: int = import_module( backend.pkg ).backendMain(ast)  # type: ignore

		if args.postCompileScript:
			if not args.postCompileScript.exists():
				warn( f'Post compile script "{args.postCompileScript}" does not exist.')
			else:
				info( f'Executing post compile script "{args.postCompileScript}"..')
				os.system( f'{sys.executable} --execpyfile {args.postCompileScript} --execpyargs {args.file.absolute()} {args.backend}' )

	except ExitError as e:
		return e.code
	return exitCode


if __name__ == '__main__':
	start = time()
	_exitCode = main()
	print( f'Done in {time() - start}' )
	exit( _exitCode )
