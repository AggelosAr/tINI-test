from typing import Any, Callable, TypeAlias

# TODO FIX 
PartialObject: TypeAlias = Callable

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str

Results: TypeAlias = dict[str, dict[str, Callable[[], None]]]

DiffMessage: TypeAlias = str
