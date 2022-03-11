"""
Module containing the CLI interface code (mainly argument parsing)
"""
import argparse
import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from typing import Optional

from platforms import Platform


class LogStyle(Enum):
	FANCY = 'fancy'
	SIMPLE = 'simple'

	def fancy( self ) -> bool:
		return self is LogStyle.FANCY


class Stage(Enum):
	TOKENIZATION = 'tokenization'
	AST = 'ast'
	BACKEND = 'backend'


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
	help='Backend to run after parsing',
	action='store',
	choices=[ elem.value for elem in Platform ],
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
	'--after-comp',
	help='Sets the python script executed after compilation to the provided file',
	action='store',
	type=Path,
	dest='postCompileScript'
)
parser.add_argument(
	'-v',
	'--verbosity',
	help='Sets the verbosity of the log (0: everything 1: warns+errors 2: errors)',
	action='store',
	# default=1,
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
parser.add_argument(
	'-dg',
	'--debug',
	help='Enables compiler debug mode',
	action='store_true',
	default=False,
	dest='debug'
)
parser.add_argument(
	'--gen-config',
	help='Creates a default config on the path specified by --config and exits',
	action='store_true',
	default=False,
	dest='genConfig'
)
parser.add_argument(
	'-l',
	'--log-style',
	help='Defines how errors and warnings indicate the line and character it originates from',
	action='store',
	default='fancy',
	choices=[ elem.value for elem in LogStyle ],
	dest='logStyle'
)
parser.add_argument(
	'--exit-at-stage',
	help='Stops execution at a given step',
	action='store',
	default='tokenization',
	choices=[ elem.value for elem in Stage ],
	dest='exitAtStage'
)
parser.add_argument(
	'--dump-tokens',
	help='Dumps the tokens generated from a file to $FILENAME.tks',
	action='store_true',
	default=False,
	dest='exitAtStage'
)
parser.add_argument(
	'--dump-ast',
	help='Dumps the ast generated from a file to $FILENAME.ast',
	action='store_true',
	default=False,
	dest='exitAtStage'
)
parser.add_argument(
	'--execpyfile',
	help=argparse.SUPPRESS,
	action='store',
	default=None,
	dest='execPyFile'
)
parser.add_argument(
	'--execpyargs',
	help=argparse.SUPPRESS,
	nargs='*',
	action='store',
	dest='execPyArgs'
)


class Arguments:
	file: Path
	backend: Platform
	showBackendHelp: bool
	configFile: Path
	postCompileScript: Optional[Path]
	interactiveMode: bool
	exitOnImplementationError: bool
	genConfig: bool
	logStyle: LogStyle
	exitAtStage: Stage
	dumpTokens: bool
	dumpAst: bool
	# 0: everything 1: warns up 2: only errors
	verboseLevel: int
	# debug mode, enable debug logging
	debug: bool
	# secret: for when we're compiled
	execPyFile: str
	execPyArgs: list[str]


# cli arguments
args: Arguments = parser.parse_args( sys.argv[ 1: ] )  # type: ignore
