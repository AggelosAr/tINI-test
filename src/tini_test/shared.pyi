from typing import Literal, Optional, overload

from tini_test.misc.annotations import (CellName, CellValue, LocalSharedScope,
                                        SharedMetaId, TestCallable,
                                        TestFunctionName)

class Cell: ...


class SharedVar:

    _stored_key: str
    _scope: Optional[TestFunctionName]

    @overload
    def __getattribute__(self, attr: Literal['__key__', '_scope']) -> CellName: ...

    @overload
    def __getattribute__(self, attr: CellName) -> Cell: ...

    @classmethod
    def add_scope(cls, shared_var: 'SharedVar', scope: TestFunctionName) -> None: ...



class MetaSharedVar:

    _test_name: Optional[TestFunctionName]
    _local_context: Optional[LocalSharedScope[SharedVar]]

    @overload
    def __getattr__(self, key: CellName) -> SharedVar | CellValue: ...

    @overload
    def __getattr__(self, key: Literal['_test_name', '_local_context']) -> TestFunctionName: ...

    @staticmethod
    def extract_meta_id() -> SharedMetaId: ...

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> LocalSharedScope[SharedVar]: ...

    @classmethod
    def extract_meta(cls, _from: TestCallable) -> 'MetaSharedVar': ...

    @classmethod
    def set_new_meta(cls, _id: SharedMetaId, apply_at: TestCallable, new_meta: 'MetaSharedVar') -> MetaSharedVar: ...

    def update_local_context(self, test_name: TestFunctionName, context: LocalSharedScope[SharedVar]) -> None: ...
