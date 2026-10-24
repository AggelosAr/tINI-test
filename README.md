# tINI test
![Coverage](.coverage.svg)
![Coverage](coverage.svg)

A lightweight Python test framework (hand-crafted and almost full type safe) focused on simple test discovery and execution from the command line with **zero dependencies**. 

The main utilities provided by the suite are:

- Defining test cases with via _@Test.case_ decorators (optional setup/cleanup).

- Adding mocks via _@Mock.mock_ decorators (mock functions/classes) or with the _Mock.mocking_ context manager.

- Adding shared/context vars via _@Shared_ decorators
    - Variables defined will be usable in any part of the code reachable from the test.

- Isolating a test via the _@Isolate_ decorators.

- Validating exceptions via the _WillRaise_ context manager.

- Asserting equality via the *must_equal* helper function.

- Running coverage.

*These utilities can be combined in any way.*

The framework was developed and tested using its' own test suite. It was also stress tested and profiled on around 10K tests to test db connections on a temp sqlite3 and management of globals. Currently the base tests that run to power the suite are ~5k (x2) (to cover almost all possible combinations) with ~500-700 unique cases. It also allows pretty prints inside the tests while running and the print verbocity modes should provide plenty of options.

## Installation

```bash
pip install tINI-test
```

## Usage

```bash
python3 -m tini_test [-r RUN MODE] [-v VERBOSITY] [-d DIRECTORY] [-f FILE] [-t TEST] [-h HELP]
```

### For coverage

Run the suite normally with the extra argments. 

> A short summary for the coverage will also be generated on the terminal.

```bash
python3 -m tini_test [--coverage] [--coverage-target] [--coverage-store]
```

Or merge multiple coverage reports into one.

```bash
python3 -m tini_test [--coverage-merge]
```

In order to generate the HTML report, run this command and point it to the generated coverage file.

This will also generate a coverage badge at the same directory with the HTML report.
```bash
python3 -m tini_test [--coverage-generate-report] [--coverage-target] [--coverage-store]
```

#### NOTES:

> `--coverage-target`, `--coverage-store` and `--coverage-merge` are all optional and accept both relative and absolute paths.

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
from tini_test import Test

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
(The items should all be passed in a similar way e.g. all as arguments or kwargs.)

If you want to pass arguments to the functions you should use a callable.

Else you can just pass the callable as is.

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
    # Or to get the traceback
    # import traceback as tb
    # traceback = context.exc_traceback
    # print(''.join(tb.format_tb(traceback)))

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

The mocking machine accepts the function to be mocked as the first argument or via the `mock` keyword, along with up to 2 keyword arguments.
Either the `returns` or a combination of `args` and `kwargs`. _Args_ must be a tuple of anything and _Kwargs_ a dict of anything.
Mocking a function call or return is as easy as:


```python
from tini_test import Test, Mock, must_equal


def f1(x, a, b):
    return x + a + b


@Mock.mock(f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Test.case
def test_mocks():
    must_equal(1 + 8 + 5, f1('?', a='?', b='?'))
               
```

The mocked function can also be supplied by keyword:

```python
@Mock.mock(mock=f1, args=(1,), kwargs={'a': 8, 'b': 5})
@Test.case
def test_mocks():
    must_equal(1 + 8 + 5, f1('?', a='?', b='?'))
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
def test_mocks():
    print('Functions! WuW')
    must_equal(c_r, func_g())
    result = func_g()()
    must_equal(999, result)

```


```python

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y

@Test.case
@Mock.mock(MyClass, args=(1, 2))
def test_mocks():
    instance = MyClass(10, 20)
    must_equal(1 + 2, instance.add())

```


```python
# Mocking class methods.
@Mock.mock(MyClass.add_more, args=(MyClass, 1_000,)) 
```


#### NOTES:
> For mocking classes only the __init__ method is manipulated. So if custom logic exists in __new__ you may need a custom mock.

> For now only mocking of initialization of a class is supported.

### Mocks can be used as context managers as well

```python
@Isolate
@Test.case
@Shared(var.a, var.b, var.c, var.d)
@Mock.mock(MyClass, args=('xyz', 'xyz'))
def test_mocking_as_context_manager_with_shared_integration():

    var.a, var.b = 1, 2
    
    with Mock.mocking(MyClass, args=(var.a, var.b)):
        '''
        .
        .
        <More mocking stacks>
        .
        .
        '''
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)
    '''
    ... <Maybe data manipulation on nested objects>
    '''

    instance = MyClass('?', '?')
    must_equal('xyz', instance.x)
    must_equal('xyz', instance.y)
```

#### NOTES:

> The mocks can be stacked in arbitrary orders. _The closer it is, the mock, to the code block, his priority should be_.

> The context manager version of _Mock_ does not make any guarantees about test pollution.
> - *To mitigate this use the* _@Isolate_ *decorator*.


### Mocks can be combined with shared

This enables a dynamic like mocking behavior

```python
@Shared(var.aa)
@Mock.mock(mocked_function, returns=(var.aa,))

or

@Shared(var.dd, var.ddd)
@Mock.mock(MyClassForDynamic, args=(var.dd,), kwargs={'y': var.ddd})

```


Here is a more complex example. The function call of func_e during the test will be proxied to the Mock as a result it will receive as args the lambda and the 1 and as kwargs the function f. Also the the top and bottom Mock decorators are ignored.

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
> Since the mock has a side effect of changing the live code object of the function, the ASYNC mode of running tests with a Mock is *Locked* e.g. an actual lock was put in place to stop global leakage to tests requesting the mocked function the time it was being mocked. In an attempt to mitigate this issue the fast solution I came up with was to simply lock it. An attempt, was also made, of parsing the _AST_ but it was hastely abandoned. (@ROADMAP)



### Adding Shared vars

Shared vars can be defined and be used in the following way

```python

from tini_test import Test, Shared, var

def side_effect_function(arg):
    var.int = arg
    return var.int


@Test.case
@Shared(var.int)
def test_side_effects():
    must_equal(NotInitialized, var.int)
    side_effect_function(456)
    must_equal(456, var.int)

```


```python

@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_smth() -> None:
    root = var.root
    ...

```

The shared vars can be used in any part of the code reachable during the lifetime of the test as long as 
the var is imported and used. e.g. `from tini_test import var`

#### Rationale
> Assume you called @Test.case with a setup callable and you retrieved a row from the db. 
The _Shared_ decorator enables you to store the item in the local context of the test and use it later.
Instead of having to do N+1 queries. 

#### NOTES
> Trying to access a variable not defined in the _Shared_ will raise _SharedVarDoesNotExistInThisContext_ 

> Trying to use global variables as var will raise _GlobalSharedVarsAreNotSupported_ 

> During async excecution, tests with shared are locked. (@ROADMAP)

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

* [ ] Make diff better.
* [ ] Add side effects to Mocks.
* [ ] Add exclude dir arg.
* [ ] Register tests into groups (group-level setup/cleanup).
* [ ] Add global fail sort mode, not just per module.
* [ ] Add support for global shared.
* [ ] Async initialization of tests.
* [ ] True Async support for mock/shared.
* [ ] Fix terminal flickering on async ( minimal )