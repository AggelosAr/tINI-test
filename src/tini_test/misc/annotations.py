from typing import Any, Callable, NamedTuple, TypeAlias, TypeVar

ColorValue: TypeAlias = str

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str

FileFailReason: TypeAlias = str


MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]

FullPythonPath: TypeAlias = str


FunctionName: TypeAlias = str

StackTrace: TypeAlias = str
DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # Callable[[Any, Any], bool]



# -------------- TIMERS --------------
TimeTakenForTestDiscovery: TypeAlias = float
TimeTakenForSuiteInitialization: TypeAlias = float
TimeTakenForTestCollection: TypeAlias = float

TimeTakenForTest: TypeAlias = float

TimeTakenToRunSuite: TypeAlias = float
# -------------- TIMERS -----------------


# -------------- SUMMARY STATS --------------
SuiteSize: TypeAlias = int
TestCollectionSize: TypeAlias = int

Successes: TypeAlias = int

Errors: TypeAlias = int

FileLoadFailures: TypeAlias = int
# -------------- SUMMARY STATS --------------



PartialObject: TypeAlias = Callable # TODO update

F_Callable: TypeAlias = Callable[..., Any] #!!!!!!!!!!
S_Callable: TypeAlias = Callable[..., Any] # Callable[[], Callable[..., Any]]

MockedFunction: TypeAlias = Callable[..., Any]



# -------------- DECORATED OBJECTS --------------
TestWrappedObject: TypeAlias = Callable[..., F_Callable] #############!
MockWrappedObject: TypeAlias = Callable[..., Any] #############!
SharedWrappedObject: TypeAlias = Callable[..., Any] #############!
# -------------- DECORATED OBJECTS --------------



_MockDefinition = TypeVar('_MockDefinition')

MockDefinitionWrapperHolder: TypeAlias = tuple[F_Callable 
                                               | MockWrappedObject 
                                               | TestWrappedObject, 
                                               _MockDefinition] | tuple[F_Callable
                                                                        | MockWrappedObject 
                                                                        | TestWrappedObject, ]




# -------------- REGISTERS --------------
HexStr = TypeVar('HexStr')

TestId   : TypeAlias = HexStr
MockId   : TypeAlias = HexStr
SharedId : TypeAlias = HexStr

T_REG: TypeAlias = dict[TestId, TestWrappedObject]
M_REG: TypeAlias = dict[MockId, Callable[..., MockDefinitionWrapperHolder]]
S_REG: TypeAlias = dict[SharedId, SharedWrappedObject]
C_REG: TypeAlias = dict[TestId | MockId, MockId | TestId]


GlobalRegistry: TypeAlias = dict[str, Any]
# -------------- REGISTERS --------------



_ReverseWrapConnections: TypeAlias = dict[MockId | TestId, set[MockId | TestId]]


class ProxyItem(NamedTuple):
    proxy: Callable[..., None]
    name: str

