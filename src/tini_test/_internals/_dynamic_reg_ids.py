import secrets
from dataclasses import dataclass

from tini_test.misc.annotations import (C_ConstRegId, I_ConstRegId,
                                        M_ConstRegId, R_M_ConstRegId,
                                        R_T_ConstRegId, S_ConstRegId,
                                        T_ConstRegId)

get_registry_key = lambda prefix, salt: '%s_%s' % (prefix, secrets.token_hex(salt))


@dataclass(frozen=True)
class TestRegistry:
    _id: T_ConstRegId


@dataclass(frozen=True)
class MockRegistry:
    _id: M_ConstRegId


@dataclass(frozen=True)
class SharedRegistry:
    _id: S_ConstRegId


@dataclass(frozen=True)
class IsolateRegistry:
    _id: I_ConstRegId


@dataclass(frozen=True)
class ConnectionRegistry:
    _id: C_ConstRegId


__T_REG = lambda salt: TestRegistry(T_ConstRegId(get_registry_key('_TEST_REGISTRY', salt)))._id
__M_REG = lambda salt: MockRegistry(M_ConstRegId(get_registry_key('_MOCK_REGISTRY', salt)))._id
__S_REG = lambda salt: SharedRegistry(S_ConstRegId(get_registry_key('_SHARED_REGISTRY', salt)))._id
__I_REG = lambda salt: IsolateRegistry(I_ConstRegId(get_registry_key('_ISOLATE_REGISTRY', salt)))._id
__C_REG = lambda salt: ConnectionRegistry(C_ConstRegId(get_registry_key('_CONNECTION_REGISTRY', salt)))._id





@dataclass(frozen=True)
class ResolvedMockRegistry:
    _id: R_M_ConstRegId


@dataclass(frozen=True)
class ResolvedTestRegistry:
    _id: R_T_ConstRegId


__R_M_REG = lambda salt: ResolvedMockRegistry(R_M_ConstRegId(get_registry_key('_RESOLVED_MOCK_REGISTRY', salt)))._id
__R_T_REG = lambda salt: ResolvedTestRegistry(R_T_ConstRegId(get_registry_key('_RESOLVED_TEST_REGISTRY', salt)))._id

