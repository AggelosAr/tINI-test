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




# ---------------- CALLABLES ----------------
# TODO FIX return types
RealTest: TypeAlias = Callable[..., Any]

SetupCallable: TypeAlias = Callable[..., Any] 
CleanupCallable: TypeAlias = Callable[..., Any]
_NoOp: TypeAlias = Callable[..., Any]


MockedFunction: TypeAlias = Callable[..., Any]


PartialObject: TypeAlias = Callable # TODO update
# ---------------- CALLABLES ----------------




# -------------- DECORATED OBJECTS --------------

# TODO args of Test.case

# Input types
TestWrappedObject   : TypeAlias = Callable[..., Any] #############! TODO return types
MockWrappedObject   : TypeAlias = Callable[..., Any] #############!
SharedWrappedObject : TypeAlias = Callable[..., Any] #############!

# DownStreamWrappedObject: ...
# UpStreamWrappedObject: ...

WrapperInput: TypeAlias = (None
                           | Callable
                           | RealTest
                           | TestWrappedObject 
                           | MockWrappedObject 
                           | SharedWrappedObject
                           | 'MockDefinitionWrappedHolder'
                           | 'SharedDefinitionHolder')


# Return types
# TODO add/fix the test return type...
TestWrappedHolder: TypeAlias = Any


_MockDefinition = TypeVar('_MockDefinition')

M1: TypeAlias = tuple[WrapperInput, _MockDefinition]
M2: TypeAlias = tuple[WrapperInput, ...]

MockDefinitionWrappedHolder: TypeAlias = M1 | M2


_SharedVar = TypeVar('_SharedVar')
SharedDefinitionHolder: TypeAlias = _SharedVar | WrapperInput
# -------------- DECORATED OBJECTS --------------




# -------------- REGISTERS --------------
HexStr = TypeVar('HexStr')

TestId   : TypeAlias = HexStr
MockId   : TypeAlias = HexStr
SharedId : TypeAlias = HexStr

T_REG: TypeAlias = dict[TestId, TestWrappedObject]
M_REG: TypeAlias = dict[MockId, Callable[..., MockDefinitionWrappedHolder]]
S_REG: TypeAlias = dict[SharedId, SharedWrappedObject]
C_REG: TypeAlias = dict[TestId | MockId, MockId | TestId]


GlobalRegistry: TypeAlias = dict[str, Any]
# -------------- REGISTERS --------------



_ReverseWrapConnections: TypeAlias = dict[MockId | TestId, set[MockId | TestId]]


class ProxyItem(NamedTuple):
    proxy: Callable[..., None]
    name: str

