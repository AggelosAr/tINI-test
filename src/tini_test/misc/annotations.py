from typing import (Any, Callable, NamedTuple, NewType, TypeAlias, TypeVar,
                    overload)

# -------------- PATHS --------------
DirectoryPath: TypeAlias = str
FileName: TypeAlias = str

DotPythonPath: TypeAlias = str
# -------------- PATHS --------------




# -------------- GENERAL -------------- < UPDATE
ColorValue: TypeAlias = str


TestFunctionName: TypeAlias = str


MappedDirectoryToTestFiles: TypeAlias = dict[DirectoryPath, list[FileName]]

FileFailReason: TypeAlias = str
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



PartialObject: TypeAlias = Callable[..., Any] #!!!!!!!!!!!!!
# ---------------- SOME CALLABLES ----------------




# -------------- DECORATED OBJECTS --------------
# Input types
TestWrappedObject    : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!
MockWrappedObject    : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!
SharedWrappedObject  : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!
IsolateWrappedObject : TypeAlias = Callable[..., 'WrapperInput'] #!!!!!!!!!!!!!


# UpStreamWrappedObject: ...
# this is wrong...
WrapperInput: TypeAlias = (None
                           | Callable
                           | RealTest
                           | TestWrappedObject 
                           | MockWrappedObject 
                           | SharedWrappedObject

                           | IsolateWrappedObject

                           | 'MockDefinitionWrappedHolder'
                           | 'SharedDefinitionHolder')
# DownStreamWrappedObject: ...

# Return types
TestWrappedHolder: TypeAlias = Callable[..., 'TestWrappedHolder']


_MockDefinition = TypeVar('_MockDefinition')
type T1[_MockDefinition] = tuple[WrapperInput, _MockDefinition]
T2: TypeAlias = tuple[WrapperInput, ]

type MockDefinitionWrappedHolder[T] = T1[T] | T2


_SharedVar = TypeVar('_SharedVar')
type T3[_SharedVar] = tuple[WrapperInput, tuple[_SharedVar]]
T4: TypeAlias = tuple[WrapperInput, ]

type SharedDefinitionHolder[T] = T3[T] | T4
# -------------- DECORATED OBJECTS --------------




# -------------- REGISTERS --------------
HexStr = TypeVar('HexStr')

TestId    : TypeAlias = HexStr
MockId    : TypeAlias = HexStr
SharedId  : TypeAlias = HexStr
IsolateId : TypeAlias = HexStr

RegisteredIds: TypeAlias = TestId | MockId | SharedId | IsolateId


T_Reg: TypeAlias = dict[TestId, TestWrappedHolder]
type M_Reg[_MockDefinition] = dict[MockId, Callable[..., MockDefinitionWrappedHolder[_MockDefinition]]]
type S_Reg[_SharedVar] = dict[SharedId, Callable[..., SharedDefinitionHolder[_SharedVar]]]
I_Reg: TypeAlias = dict[IsolateId, IsolateWrappedObject]
C_Reg: TypeAlias = dict[RegisteredIds, RegisteredIds]


T_ConstRegId = NewType('T_ConstRegId', str)
M_ConstRegId = NewType('M_ConstRegId', str)
S_ConstRegId = NewType('S_ConstRegId', str)
I_ConstRegId = NewType('I_ConstRegId', str)
C_ConstRegId = NewType('C_ConstRegId', str)


class GlobalRegistry(dict[str, Any]):

    @overload
    def __getitem__(self, key: T_ConstRegId) -> T_Reg | None: ...
    @overload
    def __getitem__(self, key: M_ConstRegId) -> M_Reg | None: ...
    @overload
    def __getitem__(self, key: S_ConstRegId) -> S_Reg | None: ...
    @overload
    def __getitem__(self, key: I_ConstRegId) -> I_Reg | None: ...
    @overload
    def __getitem__(self, key: C_ConstRegId) -> C_Reg | None: ...
    @overload
    def __getitem__(self, key: str) -> Any: ...
    def __getitem__(self, key: str) -> Any:
        return super().__getitem__(key)

    @overload  # type: ignore[override]
    def get(self, key: T_ConstRegId, default: None = None, /) -> T_Reg | None: ...
    @overload
    def get(self, key: M_ConstRegId, default: None = None, /) -> M_Reg | None: ...
    @overload
    def get(self, key: S_ConstRegId, default: None = None, /) -> S_Reg | None: ...
    @overload
    def get(self, key: I_ConstRegId, default: None = None, /) -> I_Reg | None: ...
    @overload
    def get(self, key: C_ConstRegId, default: None = None, /) -> C_Reg | None: ...
    @overload
    def get(self, key: str, default: Any = None, /) -> Any: ...
    def get(self, key: str, default: Any = None, /) -> Any:
        return super().get(key, default)

    @overload
    def __setitem__(self, key: T_ConstRegId, value: T_Reg) -> None: ...
    @overload
    def __setitem__(self, key: M_ConstRegId, value: M_Reg) -> None: ...
    @overload
    def __setitem__(self, key: S_ConstRegId, value: S_Reg) -> None: ...
    @overload
    def __setitem__(self, key: I_ConstRegId, value: I_Reg) -> None: ...
    @overload
    def __setitem__(self, key: C_ConstRegId, value: C_Reg) -> None: ...
    @overload
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)


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
type SharedVars[_SharedVar] = dict[SharedId, _SharedVar]

TestPart: TypeAlias = HexStr
type LocalSharedScope[_SharedVar] = dict[TestPart, SharedVars[_SharedVar]]

CellName: TypeAlias = str
CellValue: TypeAlias = Any
# -------------- SHARED SPECIFICS --------------


