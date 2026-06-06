from typing import Any, Callable, TypeAlias

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str


MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]


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
