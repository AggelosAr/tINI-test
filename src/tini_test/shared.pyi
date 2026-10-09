from traceback import FrameSummary
from typing import Literal, Optional, overload

from tini_test.misc.annotations import (CellName, CellValue,
                                        LocalSharedScope, SharedMetaId, TestCallable,
                                        TestFunctionName)

class Cell: ...


class SharedVar:

    _trace: list[FrameSummary]
    _stored_key: str
    _scope: Optional[TestFunctionName]

    @overload
    def __getattribute__(self, attr: Literal['_trace']) -> list[FrameSummary]: ...

    @overload
    def __getattribute__(self, attr: Literal['_stored_key']) -> Cell: ...

    @overload
    def __getattribute__(self, attr: Literal['_scope']) -> Optional[TestFunctionName]: ...

    @overload
    def __getattribute__(self, attr: Literal['__key__']) -> CellName: ...

    @overload
    def __getattribute__(self, attr: CellName) -> Cell: ...

    @classmethod
    def add_scope(cls, shared_var: 'SharedVar', scope: TestFunctionName) -> None: ...



class MetaSharedVar:

    _test_name: Optional[TestFunctionName]
    _local_context: Optional[LocalSharedScope[SharedVar]]

    _generating: bool
    _maybe_globals: list[SharedVar]

    @overload
    def __getattr__(self, attr: Literal['_test_name']) -> Optional[TestFunctionName]: ...

    @overload
    def __getattr__(self, attr: Literal['_local_context']) -> Optional[LocalSharedScope[SharedVar]]: ...

    @overload
    def __getattr__(self, attr: Literal['_generating']) -> bool: ...

    @overload
    def __getattr__(self, attr: Literal['_maybe_globals']) -> list[SharedVar]: ...

    @overload
    def __getattr__(self, key: CellName) -> SharedVar | CellValue: ...

    @staticmethod
    def extract_meta_id() -> SharedMetaId: ...

    @staticmethod
    def extract_meta(_from: TestCallable) -> MetaSharedVar: ...

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]: ...

    def raise_for_globals(self) -> None: ...

    def reset(self) -> None: ...

    def toggle(self) -> None: ...

    def update_local_context(self, test_name: TestFunctionName, context: LocalSharedScope[SharedVar]) -> None: ...

    def test_reset(self) -> None: ...
