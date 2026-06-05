from typing import Any, Callable, TypeAlias

# TODO update 
PartialObject: TypeAlias = Callable

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[..., Any] # Callable[[], Callable[..., Any]]


StackTrace: TypeAlias = str


DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # Callable[[Any, Any], bool]


ColorValue: TypeAlias = str


TestName: TypeAlias = str


TimeTakenForTestDiscoveryAndSuiteInitialization: TypeAlias = float

TimeTakenForModule: TypeAlias = float

SuiteSize: TypeAlias = int
Errors: TypeAlias = int
