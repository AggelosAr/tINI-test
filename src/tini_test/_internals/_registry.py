
from typing import Callable, Mapping

from tini_test.misc.annotations import (MockId, MockWrappedObject, TestId,
                                        TestWrappedObject)

_TEST_REGISTRY: dict[TestId, None
                             | Callable
                             | MockWrappedObject 
                             | TestWrappedObject] = {}

_MOCK_REGISTRY: dict[MockId, None
                             | Callable
                             | MockWrappedObject 
                             | TestWrappedObject] = {}

# This needs to be passed to each service... from above
_CONN: Mapping[TestId | MockId, MockId | TestId] = {}

