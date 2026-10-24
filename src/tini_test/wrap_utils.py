from collections import deque
from functools import partial
from typing import Callable, Optional, no_type_check

from tini_test._internals.consts import _I_DEC as decorators
from tini_test.misc.annotations import (I_Reg, IsolateWrappedObject, M_Reg,
                                        MockDefinitionWrappedHolder, MockId,
                                        RealTest, ResolvedMockDependencies,
                                        S_Reg, SharedDefinitionHolder,
                                        SharedId, T_Reg, TestFunctionName,
                                        TestId, TestWrappedHolder,
                                        WrapperInput, _ReverseWrapConnections)
from tini_test.misc.exceptions import (IsolateWasUsedOnWithoutTestDecorator,
                                       MockWasUsedOnWithoutTestDecorator,
                                       SharedWasUsedOnWithoutTestDecorator,
                                       TestDecoratorUsedMoreThanOnce)
from tini_test.mock import MockDefinition
from tini_test.shared import SharedVar


class DecoratedTestChain:

    def __init__(self) -> None:
        self._test_wraps: list[TestWrappedHolder] = []
        self.test_func: Optional[RealTest] = None

        self.mocks: list[MockDefinition] = []
        self._is_mock_decorated = False

        self.shared_vars: list[SharedVar] = []
        self._is_shared_decorated = False

        self.isolate = False
        self._is_isolate_decorated = False

    @property
    def has_not_dependencies(self) -> bool:
        return (
            (len(self.mocks) == 0 and not self._is_mock_decorated)
            and
            (len(self.shared_vars) == 0 and not self._is_shared_decorated) 
            and
            (not self.isolate and not self._is_isolate_decorated)
        )

    @property
    def test_wrap(self) -> TestWrappedHolder:
        return self._test_wraps[-1]

    @classmethod
    def resolve_chain(cls,
                      bi_con: _ReverseWrapConnections,
                      TEST_REGISTRY: T_Reg,
                      MOCK_REGISTRY: M_Reg,
                      SHARED_REGISTRY: S_Reg,
                      ISOLATE_REGISTRY: I_Reg,
                      /,
                      _obj_id: TestId | MockId | SharedId,) -> 'DecoratedTestChain':
    
        test_chain = DecoratedTestChain()

        visited = set()
        q = deque([_obj_id])
        
        while q:

            current_id = q.popleft()
            
            if current_id in visited:
                continue

            visited.add(current_id)

            if _next := bi_con.get(current_id):
                q.extend(_next)

            if current_id in TEST_REGISTRY:
                test_chain.add_test_wrap(TEST_REGISTRY[current_id])

            if current_id in MOCK_REGISTRY:
                mock_wrap = MOCK_REGISTRY[current_id]
                
                _test_func = test_chain.unwrap_mock(mock_wrap)

                if cls.wrap_is_test(bi_con, _test_func):
                    test_chain.test_func = _test_func
                
            if current_id in SHARED_REGISTRY:
                shared_wrap = SHARED_REGISTRY[current_id]

                _test_func = test_chain.unwrap_shared_var(shared_wrap)

                if cls.wrap_is_test(bi_con, _test_func):
                    test_chain.test_func = _test_func

            if current_id in ISOLATE_REGISTRY:
                isolate_wrap = ISOLATE_REGISTRY[current_id]
                
                _test_func = test_chain.unwrap_isolate(isolate_wrap)

                if cls.wrap_is_test(bi_con, _test_func):
                    test_chain.test_func = _test_func

        return test_chain
    
    @classmethod
    def wrap_is_test(cls, bi_con: _ReverseWrapConnections, _func: WrapperInput) -> bool:
        return hex(id(_func)) in bi_con and not cls.wrap_is_wrap(repr(_func))

    @staticmethod
    def wrap_is_wrap(_func_repr: str) -> bool:
        return any(dec in _func_repr for dec in decorators)
    
    def add_test_wrap(self, test_wrap: TestWrappedHolder):
        self._test_wraps.append(test_wrap)
    
    def unwrap_mock(self, mock_wrap: Callable[..., MockDefinitionWrappedHolder[MockDefinition]]):
        self._is_mock_decorated = True

        _test_func, *_definition = mock_wrap()

        if _definition:
            definition, *_ = _definition
            self.mocks.append(definition)

        return _test_func
    
    def unwrap_shared_var(self, shared_wrap: Callable[..., SharedDefinitionHolder[SharedVar]]):
        self._is_shared_decorated = True

        [_test_func, *_shared_holder] = shared_wrap()
                       
        if _shared_holder:
            _shared_vars, *_ = _shared_holder
            self.shared_vars.extend(_shared_vars)

        return _test_func

    def unwrap_isolate(self, isolate_wrap: IsolateWrappedObject):
        self._is_isolate_decorated = True

        _test_func = isolate_wrap()

        self.isolate = True

        return _test_func

    def raise_for_multiple_test_wraps(self) -> None:
        if len(self._test_wraps) > 1:
            _registered_test = self.test_wrap.__closure__[-1].cell_contents # type: ignore[index]

            raise TestDecoratorUsedMoreThanOnce(_registered_test)

    def raise_for_no_test_wraps(self):
        if len(self._test_wraps) == 0:

            if self._is_mock_decorated:
                raise MockWasUsedOnWithoutTestDecorator(self.test_func)
            
            if self._is_shared_decorated:
                raise SharedWasUsedOnWithoutTestDecorator(self.test_func)
            
            if self._is_isolate_decorated:
                raise IsolateWasUsedOnWithoutTestDecorator(self.test_func)  
    
    def validate_dependencies(self, test_name: TestFunctionName) -> None:
        MockDefinition.raise_for_duplicate_mocks(self.mocks, test_name)
        SharedVar.raise_for_duplicate_vars(self.shared_vars, test_name)

    @no_type_check
    def resolve_dependencies(self, 
                             MOCK_REGISTRY: M_Reg, 
                             SHARED_REGISTRY: S_Reg, 
                             ISOLATE_REGISTRY: I_Reg) -> tuple[TestFunctionName, TestWrappedHolder]:

        test_func = self.test_func
        test_wrap = self.test_wrap

        _registered_test = test_wrap.__closure__[-1].cell_contents

        if self.wrap_is_wrap(repr(_registered_test)):

            _id = hex(id(_registered_test))
            # There is the case where the last closure is the actual test pre-condition.
            # In that case we must also attach it.
            if (_id in MOCK_REGISTRY 
                or _id in SHARED_REGISTRY 
                or _id in ISOLATE_REGISTRY):

                test_wrap = partial(test_wrap, _XTest____test_func=test_func)
                test_name = test_func.__name__
            
            else:
                test_wrap.__closure__[-1].cell_contents.__code__ = test_func.__code__
                test_name = str(test_wrap.__closure__[-1].cell_contents.__name__)
        
        else:
            # We need to see if the test is already attached
            if _registered_test == test_func.__closure__[-1].cell_contents:
                test_name = _registered_test.__name__

        return test_name, test_wrap

    def add_scope(self, test_name: TestFunctionName) -> None:
        # Add shared scope for the test function
        SharedVar.add_scope(self.shared_vars, test_name)

        available_vars = {_var.__key__ for _var in self.shared_vars}
        ms_vars = []
        for mock in self.mocks:

            for _var, shard in mock._vars.items():
                if _var in available_vars:
                    ms_vars.extend(shard)

        SharedVar.add_scope(ms_vars, test_name)

        # Add mock scope for the test function
        for mock in self.mocks:
            mock.test_name = test_name

    def update_resolved_registries(self, 
                                   test_name: TestFunctionName,
                                   RESOLVED_MOCK_REGISTRY: ResolvedMockDependencies[MockDefinition]) -> None:
        if self.mocks:
            if test_name not in RESOLVED_MOCK_REGISTRY:
                RESOLVED_MOCK_REGISTRY[test_name] = []

        for mock in self.mocks:
            RESOLVED_MOCK_REGISTRY[test_name].append(mock)
