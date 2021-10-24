from dataclasses import dataclass
from typing import Optional


@dataclass
class ExitError(Exception):
	code: int
	message: Optional[str]
