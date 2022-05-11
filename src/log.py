import sys
from typing import TextIO

from cli import args as cliargs


def _log( level: int, prefix: str, msg: str, *args: object, file: TextIO ) -> None:
	if cliargs.verboseLevel <= level:
		if len( args ) == 1:
			msg = msg.replace( '{}', str( args[0] ) ).replace( '{0}', str( args[0] ) )
		else:
			for index, value in enumerate( args ):
				msg = msg.replace( f'{{{index}}}', str( value ) )
		print( f'[{prefix}] {msg}', file=file, flush=True )


def debug(msg: str, *args: object, file: TextIO = sys.stdout) -> None:
	if cliargs.debug:
		_log( 0, 'DEBUG', msg, *args, file=file )


def info(msg: str, *args: object, file: TextIO = sys.stdout) -> None:
	_log( 1, 'INFO', msg, *args, file=file )


def warn(msg: str, *args: object, file: TextIO = sys.stderr) -> None:
	_log( 2, 'WARN', msg, *args, file=file )


def error(msg: str, *args: object, file: TextIO = sys.stderr) -> None:
	_log( 3, 'ERROR', msg, *args, file=file )
