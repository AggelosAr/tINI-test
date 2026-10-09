from typing import (Any, Callable, Literal, NamedTuple, TypeAlias, TypedDict,
                    TypeVar)

# -------------- GENERAL -------------- < UPDATE
ColorValue: TypeAlias = str

DirectoryPath: TypeAlias = str
FileName: TypeAlias = str
TestFunctionName: TypeAlias = str

FileFailReason: TypeAlias = str


MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]

FullPythonPath: TypeAlias = str



StackTrace: TypeAlias = str
DiffMessage: TypeAlias = str

Comperator: TypeAlias = Callable[..., Any] # !!!!!
# -------------- GENERAL --------------




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




# ---------------- SOME CALLABLES ----------------
RealTest: TypeAlias = Callable[..., Any]

SetupCallable: TypeAlias = Callable[..., Any] 
CleanupCallable: TypeAlias = Callable[..., Any]

TestCallable: TypeAlias = RealTest | SetupCallable | CleanupCallable

_NoOp: TypeAlias = Callable[..., Any]



PartialObject: TypeAlias = Callable[..., Any] # TODO update
# ---------------- SOME CALLABLES ----------------




# -------------- DECORATED OBJECTS --------------
# Input types
TestWrappedObject   : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!
MockWrappedObject   : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!
SharedWrappedObject : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!

# DownStreamWrappedObject: ...
# UpStreamWrappedObject: ...

# this is wrong...
WrapperInput: TypeAlias = (None
                           | Callable
                           | RealTest
                           | TestWrappedObject 
                           | MockWrappedObject 
                           | SharedWrappedObject
                           | 'MockDefinitionWrappedHolder'
                           | 'SharedDefinitionHolder')


# Return types
TestWrappedHolder: TypeAlias = Any # !!!!!!!!!!!!!


_MockDefinition = TypeVar('_MockDefinition')

type T1[_MockDefinition] = tuple[WrapperInput, _MockDefinition]
T2: TypeAlias = tuple[WrapperInput, ...]

type MockDefinitionWrappedHolder[T] = T1[T] | T2

_SharedVar = TypeVar('_SharedVar')
type T3[_SharedVar] = tuple[WrapperInput, _SharedVar]
T4: TypeAlias = tuple[WrapperInput, ...]

type SharedDefinitionHolder[T] = T3[T] | T4
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


# TODO add literals and replace the hardcodes since they are already broken on edge
class GlobalRegistry(TypedDict):
    _TEST_REGISTRY   : T_REG
    _MOCK_REGISTRY   : M_REG
    _SHARED_REGISTRY : S_REG
    _CONN_REGISTRY   : C_REG
    ...

SimpleGlobalRegistry: TypeAlias = dict[str, Any]

_ReverseWrapConnections: TypeAlias = dict[RegisteredIds, set[RegisteredIds]]
# -------------- REGISTERS --------------




# -------------- MOCK SPECIFICS --------------
MockedFunction: TypeAlias = Callable[..., Any]


class ProxyItem(NamedTuple):
    proxy: Callable[..., None]
    name: str
# -------------- MOCK SPECIFICS --------------




# -------------- SHARED SPECIFICS --------------
SharedMetaId: TypeAlias = Literal['var']

type SharedVars[_SharedVar] = dict[SharedId, _SharedVar]

TestPart: TypeAlias = HexStr
type LocalSharedScope[_SharedVar] = dict[TestPart, SharedVars[_SharedVar]]

CellName: TypeAlias = str
CellValue: TypeAlias = Any
# -------------- SHARED SPECIFICS --------------


