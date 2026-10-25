from contextlib import contextmanager
from traceback import FrameSummary
from typing import Generator, Optional

from tini_test.misc.annotations import (CellName, CellValue, LocalSharedScope,
                                        TestFunctionName)

class Cell: ...


class SharedVar:

    _trace: list[FrameSummary]
    _stored_key: str
    _scope: Optional[TestFunctionName]

    @property
    def __key__(self) -> CellName: ...

    @classmethod
    def raise_for_duplicate_vars(cls, shared_vars: list['SharedVar'], test_name: TestFunctionName) -> None: ...
    
    @classmethod
    def add_scope(cls, shared_vars: list['SharedVar'], scope: TestFunctionName) -> None: ...
    

@contextmanager
def direct_access(obj: MetaSharedVar) -> Generator[MetaSharedVar, None, None]: ...


class MetaSharedVar:

    _test_name: Optional[TestFunctionName]
    _local_context: Optional[LocalSharedScope[SharedVar]]

    _generating: bool
    _maybe_globals: list[SharedVar]

    def __getattr__(self, name: CellName) -> SharedVar | CellValue: ...

    @classmethod
    def get_meta_var(cls) -> MetaSharedVar: ...

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]: ...

    def raise_for_globals(self) -> None: ...

    def reset(self) -> None: ...

    def block(self) -> None: ...

    def update_local_context(self, test_name: TestFunctionName, context: LocalSharedScope[SharedVar]) -> None: ...

    def test_reset(self) -> None: ...


class NotInitialized: ...

class Shared: ...

class var: ...
