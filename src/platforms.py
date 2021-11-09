from enum import Enum


class Platform(Enum):
	DOTNET = 'dotnet'
	INTERPRETER = 'inter'
	LLVM = 'llvm'
	WASM = 'wasm'
	NEKO = 'neko'
	JVM = 'jvm'
	PYTHON = 'py'
	JAVASCRIPT = 'js'

	@staticmethod
	def findAdeguate(name: str) -> 'Platform':
		for platform in Platform:
			if platform.value == name:
				return platform
		raise ValueError(f'Platform not found: {name}')
