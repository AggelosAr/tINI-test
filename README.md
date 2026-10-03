# tINI test
![Coverage](coverage.svg)

A lightweight Python test framework (hand-crafted) focused on simple test discovery and execution from the command line with **zero dependencies**.
The framework was developed and tested using its' own test suite. It was also stress tested and profiled on around 10K tests to test db connections on a temp sqlite3 and management of globals. It also allows pretty prints inside the tests while running and the print verbocity modes should provide plenty of options.

## Installation

```bash
pip install tINI-test
```

## Usage

```bash
python3 -m tini_test [-r RUN MODE] [-v VERBOSITY] [-d DIRECTORY] [-f FILE] [-t TEST] [-h HELP]
```

---

## Filter Combination Behavior

Filters are applied from broadest to narrowest scope:

1. Discover tests within `-d` (if provided)
2. Restrict to `-f` (if provided)
3. Restrict to `-t` (if provided)
* If used alone, the entire project is scanned.
* Options may be combined in any way.

---

## Test Registration

```python
@Test.case
def test_cats() -> None:
    ...

@Test.case()
def snakes() -> None:
    ...
```

#### NOTES:
> Multiple Test decorators on the same test will invalidate the file being tested.

The decorator accepts up to two optional callables.


```python
@Test.case(
    lambda: create_database(),
    lambda: destroy_database()
)
def test_database() -> None:
    ...

@Test.case(setup, lambda: destr())
def test_database() -> None:
    ...
```



### Catch exceptions

```python
@Test.case
def test_math() -> None:

    with WillRaise(NameError, ZeroDivisionError):   
        1/0
```
Notes: If one of the provided exceptions is not raised the test will fail and raise an `ExceptionWasNotRaised` error.

### Comparisons

```python
@Test.case
def test_list_values() -> None:

    expected = [12345]
    must_equal(expected, some_func())
```

### Combo

```python
@Test.case
def test_ints_dont_match() -> None:
    a = 10
    b = 20

    with WillRaise(_IntegerMismatchError) as context: 
        must_equal(a, b)

    must_equal('10 != 20', str(context.exception))

```


### Misc

When comparing custom objects the test suite will try to autocompare them but it is better to be explicit and pass them a callable that will apply the correct comparison.

```python
@Test.case
def test_must_equal_alien_object_with_eq() -> None:

    expected = A(11)
    actual = A(21)

    comp_func = lambda a, b: a.attr == b.attr

    must_equal(expected, actual, comp_func)

```

### Adding Mocks

The mocking machine accepts the function to be mocked as the first argument and up to 2 keyword arguments.
Either the `returns` or a combination of `args` and `kwargs`. _Args_ must be a tuple of anything and _Kwargs_ a dict of anything.
Mocking a function call or return is as easy as:


```python
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


def f1(x, a, b):
    return x + a + b

def f2(x, c, d):
    return x + c + d

def f3(x, f, g):
    return x + f + g


@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Mock.mock(f2, args=(9,), kwargs={'c': 2, 'd': 7})
@Mock.mock(f3, args=(4,), kwargs={'f': 6, 'g': 3})
@Test.case
def test_multiple_mocks_with_args():
    must_equal(1 + 8 + 5, f1('?', a='?', b='?'))
    must_equal(9 + 2 + 7, f2('?', c='?', d='?'))
    must_equal(4 + 6 + 3, f3('?', f='?', g='?'))

    must_equal(1 + 8 + 5 + 9 + 2 + 7 + 4 + 6 + 3, 
               f1('?', a='?', b='?') + 
               f2('?', c='?', d='?') + 
               f3('?', f='?', g='?'))
```

The only requirement is that all functions to be mocked are unique and imported ( else syntax error ). Also it is not possible to mock both call and return values at the same time since that would defeat the whole point of mocking I assume (@roadmap).

Here is another example. Passing arbitrary objects to the mock handler.

```python
c_r = lambda: 999
c_x = lambda: 1000

def func_g():
    return c_x

@Mock.mock(func_g, returns=c_r)
@Test.case()
def test_mock_callable_in_returns():
    print('Functions! WuW')
    must_equal(c_r, func_g())
    result = func_g()()
    must_equal(999, result)


```

Here is a more complex example. The function call of func_e during the test will be proxied to the Mock as a result it will receive as args the lambda and the 1 and as kwargs the function g. Also the the top and bottom Mock decorators are ignored.

```python

def func_e(arg1: Callable, arg2, k_val_1: Optional[Callable]=None, k_val_2=None):
    return (arg1() or 0) + arg2 + (k_val_1() if k_val_1 else 0) + (k_val_2 or 0)

def func_f():
    return 100


@Mock.mock
@Mock.mock(func_e, args=(lambda: 999, 1), kwargs={'k_val_1': lambda: func_f, 'k_val_2': None})
@Test.case
@Mock.mock()
def test_mock_anon_callable_none_in_args_kwargs():
    print('Perfect!')
    must_equal(999 + 1 + 100, func_e(func_f, 1, k_val_1=func_f, k_val_2=100))

```

#### NOTES:
> Since the mock has a side effect of changing the live code object of the function, the ASYNC mode of running tests with a Mock is *Locked* e.g. an actual lock was put in place to stop global leakage to tests requesting the mocked function the time it was being mocked. In an attempt to mitigate this issue the fast solution I came up with was to simply lock it. An attempt, was also made, of parsing the _AST_ but it was hastely abandoned. @ROADMAP.


## Test Discovery

The requested path is resolved relative to the current working directory.

A file is considered discoverable when:

* The file name begins with `test_`
* The file exists inside a directory named `tests`




### Flow

- Setup is executed before the test function runs.


- Cleanup is executed after the test function completes.

- Cleanup execution is still attempted when setup or test execution fails.

- Maybe further down the road this will be made optional by a flag.

---

### Run modes
Currently there are two modes *_sync_* amd *_async_*.
In _sync_ mode all tests run in sequential and in _async_ they run concurrently.
```bash
tini_test -r sync
```

---

### `-d DIRECTORY`

Limit test discovery to a specific directory.

```bash
tini_test -d test_math
```

All tests in the `test_math` dir will run.


---

### `-f FILE`

Limit execution to tests contained in a specific file.


```bash
python3 -m tini_test -f test_concurrency
python3 -m tini_test -f test_concurrency.py
```


Notes:
If multiple files with same name exist in different directories all will run.


---

### `-t TEST`

Run a specific test function.


```bash
python3 -m tini_test -t function_name
```


Notes:
If multiple functions with the same name are defined in different files only the first one spotted will run.

---



## Verbosity Modes

### NORMAL

Displays:

* Captured IO in the correct order
* Setup execution (if any)
* Test execution (if any)
* Cleanup execution (if any)
* Full exception details
* Stack traces
* Test discovery information
* Final summary stats
---

### SORT

Works the same way as normal. But failures are sorted to the bottom.

The sorting is only applied per module . 

*Maybe further down the road a flag to sort globally may be introduced.

---

### MINIMAL

Minimal display:

* Failed tests ( names only )
* Associated stack traces
* Final execution summary


`MINIMAL_NO_STACK` is same as `MINIMAL`, except that no stack traces are shown.
`SUPER_MINIMAL` is same as `MINIMAL_NO_STACK` but less verbose.

---


## Notes


While the discovery implementation will find tests with the same names or sub dirs with same names or even actual tests cases with same names, it is heavily discouraged.

Of course the above is somewhat cancelled because the algorithm tries to autocomplete the path, as a result when searching for a sub directory that exists in multiple sub directories with the same name, no guarantees are made that all tests will be excecuted.


---


## Roadmap

* [ ] Add test context/shared vars.
* [ ] Add side effects to Mocks.
* [ ] Add exclude dir arg.
* [ ] Register tests into groups (group-level setup/cleanup).
* [ ] Add global fail sort mode, not just per module.
