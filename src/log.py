import sys
from typing import TextIO

from cli import args


def _log(level: int, msg: str, file: TextIO) -> None:
	if args.verboseLevel <= level:
		print(msg, file=file)


def debug(msg: str, file: TextIO = sys.stdout) -> None:
	if args.debug:
		_log( 0, f'[DEBUG] {msg}', file )


def info(msg: str, file: TextIO = sys.stdout) -> None:
	_log( 1, f'[INFO] {msg}', file )


def warn(msg: str, file: TextIO = sys.stderr) -> None:
	_log( 2, f'[WARN] {msg}', file )


def error(msg: str, file: TextIO = sys.stderr) -> None:
	_log( 3, f'[ERROR] {msg}', file )
