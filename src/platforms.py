from enum import Enum
from typing import Union


class Platform(Enum):
	DOTNET = 'dotnet'
	INTERPRETER = 'inter'
	LLVM = 'llvm'
	WASM = 'wasm'
	NEKO = 'neko'
	JVM = 'jvm'
	PYTHON = 'py'
	JAVASCRIPT = 'js'

	@classmethod
	def findAdeguate( cls, name: Union[ str, 'Platform' ] ) -> 'Platform':
		if isinstance( name, Platform ):
			return name
		for platform in cls:
			if platform.value == name:
				return platform
		raise ValueError(f'Platform not found: {name}')
