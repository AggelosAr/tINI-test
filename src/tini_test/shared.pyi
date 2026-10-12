from traceback import FrameSummary
from typing import Literal, Optional, overload

from tini_test.misc.annotations import (CellName, CellValue, LocalSharedScope,
                                        SharedMetaId, TestCallable,
                                        TestFunctionName)

class Cell: ...


class SharedVar:

    _trace: list[FrameSummary]
    _stored_key: str
    _scope: Optional[TestFunctionName]

    def __key__(self) -> CellName: ...

    @classmethod
    def add_scope(cls, shared_var: 'SharedVar', scope: TestFunctionName) -> None: ...



class MetaSharedVar:

    _test_name: Optional[TestFunctionName]
    _local_context: Optional[LocalSharedScope[SharedVar]]

    _generating: bool
    _maybe_globals: list[SharedVar]

    @classmethod
    def get_meta_var(cls) -> MetaSharedVar: ...

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]: ...

    def raise_for_globals(self) -> None: ...

    def reset(self) -> None: ...

    def block(self) -> None: ...

    def update_local_context(self, test_name: TestFunctionName, context: LocalSharedScope[SharedVar]) -> None: ...

    def test_reset(self) -> None: ...
