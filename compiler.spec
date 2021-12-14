# -*- mode: python ; coding: utf-8 -*-
# from PyInstaller.building.api import PYZ, EXE, COLLECT
# from PyInstaller.building.build_main import Analysis


DEBUG: bool = True


analysis = Analysis(
	[ 'src\\compiler.py' ],
	pathex=[ ],
	binaries=[ ],
	datas=[ ],
	hiddenimports=[
		'ast_',
		'backend.interpreter',
		'backend.llvm',
		'backend.wasm',
	],
	hookspath=[ ],
	hooksconfig={},
	runtime_hooks=[ ],
	excludes=[
		'asyncio',
		'bz2',
		'socket',
		'ssl',
		'lzma',
	],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	noarchive=False
)

pyz = PYZ(
	analysis.pure,
	analysis.zipped_data,
	cipher=None
)

exe = EXE(
	pyz,
	analysis.scripts,
	[ ],
	exclude_binaries=True,
	name='endcc',
	debug=DEBUG,
	bootloader_ignore_signals=False,
	strip=not DEBUG,
	upx=not DEBUG,
	console=True,
	disable_windowed_traceback=False,
	target_arch=None,
	codesign_identity=None,
	entitlements_file=None
)

coll = COLLECT(
	exe,
	analysis.binaries,
	analysis.zipfiles,
	analysis.datas,
	strip=not DEBUG,
	upx=not DEBUG,
	upx_exclude=[ ],
	name='endcc'
)
