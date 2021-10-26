"""
Contains info about the compiler backends and a abstract class representing them.
"""

from dataclasses import dataclass

from ast_.expr import Expr


class Backend:
	@staticmethod
	def backendMain(ast: Expr) -> int:
		"""
		Main function for a backend
		\t
		:param ast:
		:return: exit code
		"""


@dataclass
class BackendInfo:
	name: str
	pkg: str
	help: str
	available: bool


BACKENDS: dict[ str, BackendInfo ] = {
	'inter': BackendInfo(
		name='Interpreter',
		pkg='backend.interpreter',
		help='Directly interpret the source code',
		available=True
	),
	'llvm': BackendInfo(
		name='LLVM',
		pkg='backend.llvm',
		help='Compiles to LLVM IR and then to machine code',
		available=False
	),
	'wasm': BackendInfo(
		name='WASM',
		pkg='backend.wasm',
		help='Compiles to WASM text format and then to binary',
		available=False
	),
	'py': BackendInfo(
		name='Python 3.9 VM',
		pkg='backend.py',
		help='Compiles to python bytecode (.pyc files)',
		available=False
	),
	'jvm': BackendInfo(
		name='Java Virtual Machine',
		pkg='backend.jvm',
		help='Compiles to JVM bytecode (.class files)',
		available=False
	),
	'neko': BackendInfo(
		name='Neko VM',
		pkg='backend.neko',
		help='Compiles to the Neko VM bytecode',
		available=False
	),
	'js': BackendInfo(
		name='JavaScript',
		pkg='backend.js',
		help='Transpiles to js code',
		available=False
	)
}
