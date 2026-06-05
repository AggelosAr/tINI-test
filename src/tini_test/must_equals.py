import enum
from collections import deque
from difflib import unified_diff
from functools import lru_cache
from typing import Any, Optional, assert_never

from .misc.annotations import Comperator
from .misc.exceptions import (ComperatorIsNotValid, ComperatorWasNotProvided,
                              ExpectedWasDifferentFromActual)

_known_types = set([type,
                    bool,
                    int,
                    float,
                    str,
                    set,
                    tuple,
                    list,
                    dict])

here = None

_diff_threshold = 2**16

_max_m_l_diffs = 3

_max_line_context = 100

_S = 1000

# =========================================================
# Public API
# =========================================================


def must_equal(expected: Any, 
               actual: Any, 
               comperator: Optional[Comperator | Any] = None) -> None:
    '''
    Assert that expected and actual are equal.

    Primitive values and built-in containers (str, list, tuple, set,
    dict, etc.) are compared recursively and a human-friendly diff is
    produced when a mismatch is found. If provided, the comperator is always used instead of the
    built-in comparison logic. The comperator must return
    ``True`` when the values should be considered equal and
    ``False`` otherwise.
    '''
    # format the exception to stop at the user level.
    
    try:
        if comperator:
            _assert_comperator(comperator)
            
        _must_equal(expected=expected,
                    actual=actual, 
                    path='ITEM',
                    comperator=comperator)

    except ExpectedWasDifferentFromActual as e:
        raise ExpectedWasDifferentFromActual(e._get_detail()) from here
    
    except ComperatorWasNotProvided:
        raise ComperatorWasNotProvided from here
    
    except ComperatorIsNotValid as e:
        raise ComperatorIsNotValid(str(e)) from here
    

# =========================================================
# Helpers
# =========================================================

@lru_cache(maxsize=None)
def _assert_comperator(comperator: Comperator | Any) -> None:

    if '__code__' not in dir(comperator):
        raise ComperatorIsNotValid(reason='Comperator is not a function')
    
    if comperator.__code__.co_argcount != 2:
        raise ComperatorIsNotValid(reason='Comperator must accept two items')
    
    return

    from dis import Bytecode, dis  # TODO

    # Review compare ops 
    _TRUE_LOAD = 'LOAD_CONST1(True)'           #
    _FALSE_LOAD = 'LOAD_CONST2(False)'         #
    _COMPARE_OP = '_COMPARE_OP72(==)'          #
    _COMPARE_OP_2 = 'COMPARE_OP2(==)'          #
    _RETURN = 'RETURN_VALUE'                   #
    # dis ->  With no argument, disassemble the last traceback
    data = Bytecode(comperator).dis().split('\n')
    data = list(map(lambda l: l.replace(' ', ''), data))
    data = list(filter(lambda l: l != '', data))

    has_loads = False
    has_loads_idx = -1

    for idx, line in enumerate(data):
        
        if any([_TRUE_LOAD in line,
                _FALSE_LOAD in line,
                _COMPARE_OP in line,
                _COMPARE_OP_2 in line]):
            has_loads = True
            has_loads_idx = idx
            continue

        if all([_RETURN in line,
                has_loads,
                idx-1 == has_loads_idx]):
            return

    raise ComperatorIsNotValid


def _raise_diff(msg: str) -> None:
    raise ExpectedWasDifferentFromActual(msg)


def _unified_diff(expected: str, actual: str) -> str:
    expected = str(expected)
    actual = str(actual)

    if '\n' in expected or '\n' in actual:
        return _multiline_diff(expected, actual)

    return _single_line_diff(expected, actual)


def _multiline_diff(expected: str, actual: str) -> str:

    lines = list(
        unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile='expected',
            tofile='actual',
        )
    )


    result = []
    hunk_count = 0

    _expected = []
    _actual = deque()
    

    for idx in range(len(lines)):

        line = lines[idx]
        if line.startswith('@@'):
            
            hunk_count += 1

            if hunk_count > _max_m_l_diffs:
              
                result.append(
                    '\n... additional differences omitted (%s+ more) ...\n' 
                    % (hunk_count - _max_m_l_diffs, )
                )
                break
            
            __x = '~~~~~~~~~~~~~~~~~~~~~~~~'
            result.append('\n%s\n%s\n%s\n' % (__x, line, __x, ))
         

        elif line.startswith('-') and not line.startswith('--'):
            

            line = line[1:]

            if _actual:
                
                if line != (_v := _actual.popleft()):

                    r = _single_line_diff(line, _v)

                    result.append('\n%s\n' % (r, ))

            else:
                
                _expected.append(line)
            
          
        elif line.startswith('+') and not line.startswith('++'):
            

            line = line[1:]

            if _expected:
             
                if line != (_v := _expected.pop()):

                    r = _single_line_diff(_v, line)
            
                    result.append('\n%s\n' % (r, ))

            else:

                _actual.append(line)

        else:
            if (l := len(line)) > _max_line_context:
                # Truncate line here
                line = ('%s[TRUNCATED<%s>chars]%s' 
                        % (lines[idx][:_max_line_context//2], 
                            '%d' % (t, )
                            if (t := l - _max_line_context) <= _S
                            else '%d+' % (min(_S, t), ), 
                            lines[idx][-_max_line_context//2:], ))

            result.append(line)
            
    return ''.join(result)


def _single_line_diff(expected: str, actual: str) -> str:
    
    for idx, (e, a) in enumerate(zip(expected, actual)):
        if e != a:
            break
    else:
        idx = min(len(expected), len(actual))

    start = max(0, idx - _max_line_context)
    end = idx + _max_line_context

    exp_snippet = expected[start:end]
    act_snippet = actual[start:end]

    exp_char = (
        repr(expected[idx])
        if idx < len(expected)
        else '<end-of-string>'
    )

    act_char = (
        repr(actual[idx])
        if idx < len(actual)
        else '<end-of-string>'
    )

    return (
        'string mismatch at index %d\n'
        'expected char: %s\n'
        'actual char:   %s\n'
        '\n'
        'expected: %r'
        '\n'
        'actual:   %r'
        '\n'
        '          %s^'
    ) % (
        idx,
        exp_char,
        act_char,
        exp_snippet,
        act_snippet,
        ' ' * (idx - start + 1), # TODO if char is excaped +1 
    )

# =========================================================
# Core dispatcher
# =========================================================


def _must_equal(expected: Any, 
                actual: Any, 
                path: str,
                comperator: Optional[Comperator] = None) -> None:

    if expected is None and actual is None:
        return

    if type(expected) != type(actual):
        _raise_diff(
            '%s: type mismatch\nexpected: %s\nactual:   %s'
            % (path, type(expected), type(actual), )
        )
        return

    _is_alien = type(expected) not in _known_types

    # If no comperator is provided we will try to discover it.
    if not comperator and type(expected) == type(actual) and _is_alien:
        
        # If it is known enum we just have to compare them.
        if issubclass(expected.__class__, enum.Enum):
            _diff_enum(expected, actual, path)
            return
        
        if '__eq__' in dir(expected):
            
            # Determine is __eq__ is implemented on that class.
            if expected.__eq__(actual) is NotImplemented:
                raise ComperatorWasNotProvided

            if expected.__eq__(actual):
                return
            else:
                # case of alien primitive or alien?
                _diff_alien_primitive(expected, actual, path) # type: ignore[arg-type]
                return
            
        raise ComperatorWasNotProvided
    

    if _is_alien:
        _diff_alien_primitive(expected, actual, path, comperator) # type: ignore[arg-type]
        return
    
    if isinstance(expected, type):
        _diff_primitive(expected, actual, path)
        return
    
    if isinstance(expected, bool):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, int):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, float):
        _diff_primitive(expected, actual, path)
        return

    if isinstance(expected, str):
        _diff_str(expected, actual, path)
        return
    
    if isinstance(expected, set):
        _diff_set(expected, actual, path)
        return

    if isinstance(expected, tuple):
        _diff_tuple(expected, actual, path, comperator)
        return

    if isinstance(expected, list):
        _diff_list(expected, actual, path, comperator)
        return

    if isinstance(expected, dict):
        _diff_dict(expected, actual, path, comperator)
        return

    assert_never(expected)


# =========================================================
# Primitive types
# =========================================================


def _diff_enum(expected: enum.Enum, actual: enum.Enum, path: str) -> None:
    if expected.value != actual.value:
        _raise_diff('%r != %r' % (expected, actual, ))
        return


def _diff_primitive(expected: Any, actual: Any, path: str) -> None:
    if expected != actual:
        _raise_diff('%r != %r' % (expected, actual, ))
        return


def _diff_str(expected: str, actual: str, path: str) -> None:
    if expected == actual:
        return

    if len(expected) > _diff_threshold or len(actual) > _diff_threshold:
        _raise_diff('String mismatch')
        return
    
    diff = _unified_diff(expected, actual)
    _raise_diff('%s:\n%s' % (path, diff, ))
    return


def _diff_alien_primitive(expected: Any, 
                          actual: Any, 
                          path: str,
                          comperator: Optional[Comperator]=None) -> None:

    # TODO maybe use the str or repr if it is defined?
    if not comperator or comperator(expected, actual) is False:

        _raise_diff('%s: %s != %s' 
                    % (path, 
                       '<Object %s at %s>' 
                       % (expected.__class__.__name__, 
                          hex(id(expected)), ), 
                       '<Object %s at %s>' 
                       % (actual.__class__.__name__, 
                          hex(id(actual)), ), ))
        return


# =========================================================
# Containers
# =========================================================


def _diff_set(expected: set[Any], 
              actual: set[Any], 
              path: str) -> None:

    if expected == actual:
        return

    missing = expected - actual
    extra = actual - expected

    _raise_diff(
        '%s: set mismatch\nmissing: %r\nextra: %r'
        % (path, missing, extra, )
    )
    return


def _diff_tuple(expected: tuple[Any, ...], 
                actual: tuple[Any, ...], 
                path: str,
                comperator: Optional[Comperator]) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            'tuple length mismatch\nexpected=%d actual=%d'
            % (len(expected), len(actual), )
        )
        return

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i, ), comperator)


def _diff_list(expected: list[Any], 
               actual: list[Any], 
               path: str,
               comperator: Optional[Comperator]) -> None:

    if len(expected) != len(actual):
        _raise_diff(
            'list length mismatch\nexpected=%d actual=%d'
            % (len(expected), len(actual), )
        )
        return

    for i, (e, a) in enumerate(zip(expected, actual)):
        _must_equal(e, a, '%s[%d]' % (path, i, ), comperator)


def _diff_dict(expected: dict[Any, Any], 
               actual: dict[Any, Any], 
               path: str,
               comperator: Optional[Comperator]) -> None:

    if expected.keys() != actual.keys():
        missing = expected.keys() - actual.keys()
        extra = actual.keys() - expected.keys()

        _raise_diff(
            '%s: dict key mismatch\nmissing: %r\nextra: %r'
            % (path, missing, extra, )
        )
        return

    for key in expected:
        _must_equal(expected[key], actual[key], '%s[%r]' % (path, key, ), comperator)
