from typing import Any, Callable, TypeAlias

ColorValue: TypeAlias = str

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str

MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]

FullPythonPath: TypeAlias = str

TimeTakenForTestDiscovery: TypeAlias = float

# These are the same thing
TimeTakenForSuiteInitialization: TypeAlias = float
TimeTakenForTestCollection: TypeAlias = float

TimeTakenForTest: TypeAlias = float

TimeTakenToRunSuite: TypeAlias = float


PartialObject: TypeAlias = Callable # TODO update

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[..., Any] # Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str
DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # Callable[[Any, Any], bool]


SuiteSize: TypeAlias = int
TestCollectionSize: TypeAlias = int
Successes: TypeAlias = int
Errors: TypeAlias = int
Failures: TypeAlias = int
