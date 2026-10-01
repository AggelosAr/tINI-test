
from typing import Callable, TypeAlias, TypeVar

from tini_test.misc.annotations import (F_Callable, MockId, MockWrappedObject,
                                        TestId, TestWrappedObject)

# TODO these registers should be per module?
_TEST_REGISTRY: dict[TestId, TestWrappedObject] = {}


_MockDefinition = TypeVar('_MockDefinition')

MockDefinitionWrapperHolder: TypeAlias = tuple[F_Callable 
                                               | MockWrappedObject 
                                               | TestWrappedObject, 
                                               _MockDefinition] | tuple[F_Callable
                                                                        | MockWrappedObject 
                                                                        | TestWrappedObject, ]

_MOCK_REGISTRY: dict[MockId, Callable[..., MockDefinitionWrapperHolder]] = {}

# This needs to be passed to each service... from above
_CONN: dict[TestId | MockId, MockId | TestId] = {}

