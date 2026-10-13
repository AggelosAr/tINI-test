import secrets
from dataclasses import dataclass

from tini_test.misc.annotations import (C_ConstRegId, I_ConstRegId,
                                        M_ConstRegId, S_ConstRegId,
                                        T_ConstRegId)

get_registry_key = lambda prefix: '%s_%s' % (prefix, secrets.token_hex(5))


@dataclass
class TestRegistry:
    _id: T_ConstRegId


@dataclass
class MockRegistry:
    _id: M_ConstRegId


@dataclass
class SharedRegistry:
    _id: S_ConstRegId


@dataclass
class IsolateRegistry:
    _id: I_ConstRegId


@dataclass
class ConnectionRegistry:
    _id: C_ConstRegId


__T_REG = TestRegistry(T_ConstRegId(get_registry_key('_TEST_REGISTRY')))._id
__M_REG = MockRegistry(M_ConstRegId(get_registry_key('_MOCK_REGISTRY')))._id
__S_REG = SharedRegistry(S_ConstRegId(get_registry_key('_SHARED_REGISTRY')))._id
__I_REG = IsolateRegistry(I_ConstRegId(get_registry_key('_ISOLATE_REGISTRY')))._id
__C_REG = ConnectionRegistry(C_ConstRegId(get_registry_key('_CONNECTION_REGISTRY')))._id

