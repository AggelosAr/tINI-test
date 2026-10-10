from tini_test._internals.consts import _C_REG, _I_REG, _M_REG, _S_REG, _T_REG
from tini_test.enums import Plugs
from tini_test.misc.annotations import (C_REG, I_REG, M_REG, S_REG, T_REG,
                                        GlobalRegistry, SimpleGlobalRegistry)


def attach_state(source_obj: GlobalRegistry, 
                 target_obj: SimpleGlobalRegistry | GlobalRegistry,
                 /,
                 *,
                 mode: Plugs) -> tuple[T_REG 
                                       | M_REG 
                                       | S_REG 
                                       | I_REG, C_REG]:

    _test_reg   : T_REG = source_obj.get(_T_REG)
    _mock_reg   : M_REG = source_obj.get(_M_REG)
    _shared_reg : S_REG = source_obj.get(_S_REG)

    _isol_reg   : I_REG = source_obj.get(_I_REG)
    
    _conn_reg   : C_REG = source_obj.get(_C_REG)

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
