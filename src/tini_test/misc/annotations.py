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

# TODO Fix this type.
TestCallables: TypeAlias = SetupCallable | SetupCallable | CleanupCallable | _NoOp

MockedFunction: TypeAlias = Callable[..., Any]


PartialObject: TypeAlias = Callable # TODO update
# ---------------- CALLABLES ----------------




# -------------- DECORATED OBJECTS --------------

# TODO args of Test.case

# Input types
TestWrappedObject   : TypeAlias = Callable[..., 'WrapperInput'] #############! TODO return types
MockWrappedObject   : TypeAlias = Callable[..., 'WrapperInput'] #############!
SharedWrappedObject : TypeAlias = Callable[..., 'WrapperInput'] #############!

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
M3: TypeAlias = tuple[WrapperInput, _SharedVar]
M4: TypeAlias = tuple[WrapperInput, ...]
SharedDefinitionHolder: TypeAlias = M3 | M4
# -------------- DECORATED OBJECTS --------------




# -------------- REGISTERS --------------
HexStr = TypeVar('HexStr')

TestId   : TypeAlias = HexStr
MockId   : TypeAlias = HexStr
SharedId : TypeAlias = HexStr

RegisteredIds: TypeAlias = TestId | MockId | SharedId

T_REG: TypeAlias = dict[TestId, TestWrappedObject]
M_REG: TypeAlias = dict[MockId, Callable[..., MockDefinitionWrappedHolder]]
S_REG: TypeAlias = dict[SharedId, SharedWrappedObject]

C_REG: TypeAlias = dict[RegisteredIds, RegisteredIds]


GlobalRegistry: TypeAlias = dict[str, Any]

_ReverseWrapConnections: TypeAlias = dict[RegisteredIds, set[RegisteredIds]]
# -------------- REGISTERS --------------



class ProxyItem(NamedTuple):
    proxy: Callable[..., None]
    name: str

