from typing import Any, Callable, TypeAlias

#rom src.utils import TestSuite

TestsContainer: TypeAlias = dict[str, dict[str, 'TestSuite']]

F_Callable: TypeAlias = Callable[..., Any]
S_Callable: TypeAlias = Callable[[], Callable[..., Any]]

StackTrace: TypeAlias = str
