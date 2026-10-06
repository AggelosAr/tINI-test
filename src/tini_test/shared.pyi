from typing import Literal, overload

from tini_test.misc.annotations import CellName, CellValue
from tini_test.shared import Cell

# TODO

class SharedVar:

    @overload
    def __getattribute__(self, attr: Literal['__key__']) -> CellName: ...

    @overload
    def __getattribute__(self, attr: str) -> Cell: ...



class MetaSharedVar:

    @overload
    def __getattr__(self, attr: Literal['_context']) -> SharedVar: ...

    @overload
    def __getattr__(self, attr: str) -> CellValue: ...
