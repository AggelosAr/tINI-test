from typing import Any, Callable, TypeAlias

# TODO update 
PartialObject: TypeAlias = Callable

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[..., Any]
#S_Callable: TypeAlias = Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str


DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[[Any, Any], bool]
