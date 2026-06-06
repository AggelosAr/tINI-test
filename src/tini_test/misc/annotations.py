from typing import Any, Callable, TypeAlias


ColorValue: TypeAlias = str

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str

MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]


TimeTakenForTestDiscovery: TypeAlias = float
TimeTakenForSuiteInitialization: TypeAlias = float


PartialObject: TypeAlias = Callable # TODO update

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[..., Any] # Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str
DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # Callable[[Any, Any], bool]


SuiteSize: TypeAlias = int
Errors: TypeAlias = int
