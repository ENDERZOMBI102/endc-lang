"""
Interpreter error handler
"""

import traceback


def getTracebackText(e: Exception) -> str:
	return '\n'.join(
		traceback.format_exception(
			type( e ),
			e,
			e.__traceback__
		)
	)
