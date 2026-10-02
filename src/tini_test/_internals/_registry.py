from typing import Literal

from tini_test.misc.annotations import C_REG, M_REG, T_REG, GlobalRegistry


def attach_state(source_obj: GlobalRegistry, 
                 target_obj: GlobalRegistry,
                 mode: Literal['mock', 'test'] ) -> None:

    _test_reg: T_REG = source_obj.get('_TEST_REGISTRY')
    _mock_reg: M_REG = source_obj.get('_MOCK_REGISTRY')
    _conn_reg: C_REG = source_obj.get('_CONN_REGISTRY')
    
    target_obj['_TEST_REGISTRY'] = _test_reg
    target_obj['_MOCK_REGISTRY'] = _mock_reg
    target_obj['_CONN_REGISTRY'] = _conn_reg

    if mode=='mock':
        return _mock_reg, _conn_reg
    elif mode=='test':
        return _test_reg, _conn_reg
