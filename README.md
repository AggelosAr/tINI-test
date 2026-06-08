![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AggelosAr/9f0a75f4e7d7a1fb8ef58c41edbad054/raw/covbadge.json)


# tINI test

A lightweight Python test framework focused on simple test discovery and execution from the command line.
The framework was tested using its own test suite and has 100% coverage. It was also stress tested on around 1K tests to test db connections on a temp sqlite3. It also allows pretty prints inside the tests while running.

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

* [ ] Register tests into groups (group-level setup/cleanup)
* [ ] Add global fail sort mode, not just per module.
* [ ] Add exclude dir arg