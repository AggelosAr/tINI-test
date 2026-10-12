from typing import Literal, overload

from tini_test._internals.consts import _C_REG, _I_REG, _M_REG, _S_REG, _T_REG
from tini_test.enums import Plugs
from tini_test.misc.annotations import (C_Reg, GlobalRegistry, I_Reg, M_Reg,
                                        S_Reg, SimpleGlobalRegistry, T_Reg)


@overload
def attach_state(source_obj: GlobalRegistry,
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Literal[Plugs.TEST]) -> tuple[T_Reg | None, C_Reg | None]: ...
@overload
def attach_state(source_obj: GlobalRegistry,
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Literal[Plugs.MOCK]) -> tuple[M_Reg | None, C_Reg | None]: ...
@overload
def attach_state(source_obj: GlobalRegistry,
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Literal[Plugs.SHARED]) -> tuple[S_Reg | None, C_Reg | None]: ...
@overload
def attach_state(source_obj: GlobalRegistry,
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Literal[Plugs.ISOLATE]) -> tuple[I_Reg | None, C_Reg | None]: ...
def attach_state(source_obj: GlobalRegistry,
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Plugs) -> tuple[T_Reg | M_Reg | S_Reg | I_Reg | None, 
                                       C_Reg | None]:

    _test_reg   = source_obj.get(_T_REG)
    _mock_reg   = source_obj.get(_M_REG)
    _shared_reg = source_obj.get(_S_REG)
    _isol_reg   = source_obj.get(_I_REG)
    _conn_reg   = source_obj.get(_C_REG)

    target_obj[_T_REG] = _test_reg
    target_obj[_M_REG] = _mock_reg
    target_obj[_S_REG] = _shared_reg
    target_obj[_I_REG] = _isol_reg
    target_obj[_C_REG] = _conn_reg

    match mode:

        case Plugs.TEST:
            return _test_reg, _conn_reg
        
        case Plugs.MOCK:
            return _mock_reg, _conn_reg
        
        case Plugs.SHARED:
            return _shared_reg, _conn_reg
        
        case Plugs.ISOLATE:
            return _isol_reg, _conn_reg
