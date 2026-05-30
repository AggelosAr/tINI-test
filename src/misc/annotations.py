from typing import Any, Callable, TypeAlias

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str
