from typing import Any, Callable, TypeAlias

F_Callable: TypeAlias = Callable[[Any], Any]
S_Callable: TypeAlias = Callable[[Callable[[Any], None]], None]
