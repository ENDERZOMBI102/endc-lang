"""
Module containing the CLI interface code (mainly argument parsing)
"""

import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Literal

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
parser.add_argument(
	'--exit-on-error',
	help='Makes the interpreter exits when a implementation error occurs',
	action='store_true',
	default=False,
	dest='exitOnImplementationError'
)


class Arguments:
	file: Path
	backend: Literal['inter', 'llvm', 'wasm', 'py', 'jvm', 'neko', 'js']
	showBackendHelp: bool
	configFile: Path
	postCompileScript: Optional[Path]
	interactiveMode: bool
	exitOnImplementationError: bool
	# 0: everything 1: warns up 2: only errors
	verboseLevel: int


# cli arguments
args: Arguments = parser.parse_args( sys.argv[ 1: ] )  # type: ignore
