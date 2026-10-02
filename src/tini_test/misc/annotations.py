from typing import Any, Callable, NamedTuple, TypeAlias, TypeVar

ColorValue: TypeAlias = str

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str

FileFailReason: TypeAlias = str


MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]

FullPythonPath: TypeAlias = str

TimeTakenForTestDiscovery: TypeAlias = float

# These are the same thing
TimeTakenForSuiteInitialization: TypeAlias = float
TimeTakenForTestCollection: TypeAlias = float

TimeTakenForTest: TypeAlias = float

TimeTakenToRunSuite: TypeAlias = float


PartialObject: TypeAlias = Callable # TODO update

F_Callable: TypeAlias = Callable[..., Any] #!!!!!!!!!!
S_Callable: TypeAlias = Callable[..., Any] # Callable[[], Callable[..., Any]]


StackTrace: TypeAlias = str
DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # Callable[[Any, Any], bool]


SuiteSize: TypeAlias = int
TestCollectionSize: TypeAlias = int
Successes: TypeAlias = int
Errors: TypeAlias = int

FileLoadFailures: TypeAlias = int


MockWrappedObject: TypeAlias = Callable[..., Any] #############!
TestWrappedObject: TypeAlias = Callable[..., F_Callable] #############!


MockedFunction: TypeAlias = Callable[..., Any]


HexStr = TypeVar('HexStr')
TestId: TypeAlias = HexStr
MockId: TypeAlias = HexStr

_ReverseWrapConnections: TypeAlias = dict[MockId | TestId, set[MockId | TestId]]


_MockDefinition = TypeVar('_MockDefinition')

MockDefinitionWrapperHolder: TypeAlias = tuple[F_Callable 
                                               | MockWrappedObject 
                                               | TestWrappedObject, 
                                               _MockDefinition] | tuple[F_Callable
                                                                        | MockWrappedObject 
                                                                        | TestWrappedObject, ]


class ProxyItem(NamedTuple):
    proxy: Callable[..., None]
    name: str


T_REG: TypeAlias = dict[TestId, TestWrappedObject]
M_REG: TypeAlias = dict[MockId, Callable[..., MockDefinitionWrapperHolder]]
C_REG: TypeAlias = dict[TestId | MockId, MockId | TestId]


GlobalRegistry: TypeAlias = dict[str, Any]


FunctionName: TypeAlias = str
