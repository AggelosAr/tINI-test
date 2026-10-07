from typing import Literal, overload

from tini_test.misc.annotations import (CellName, CellValue, SharedMetaId,
                                        SharedScope, TestCallables,
                                        TestFunctionName)

class Cell: ...


class SharedVar:

    # __key__: CellName

    @overload
    def __getattribute__(self, attr: Literal['__key__']) -> CellName: ...

    @overload
    def __getattribute__(self, attr: str) -> Cell: ...



class MetaSharedVar:

    @overload
    def __getattr__(self, attr: Literal['_test_name']) -> TestFunctionName: ...
    
    @overload
    def __getattr__(self, attr: Literal['_context']) -> SharedScope[SharedVar]: ...

    @overload
    def __getattr__(self, attr: str) -> CellValue: ...

    @staticmethod
    def extract_meta() -> SharedMetaId: ...

    @staticmethod
    def get_context_from_shards(shards: list[SharedVar]) -> SharedScope[SharedVar]: ...

    @classmethod
    def with_context(cls, test_name: TestFunctionName, context: SharedScope[SharedVar]) -> MetaSharedVar: ...

    @classmethod
    def set_new_meta(cls, _id: SharedMetaId, apply_at: TestCallables, new_meta: 'MetaSharedVar') -> MetaSharedVar: ...

