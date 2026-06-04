# tINI test

A lightweight Python test framework focused on simple test discovery and execution from the command line.
The framework was tested using its own test suite.
## Usage

```bash
tini_test [VERBOSITY] [-d DIRECTORY] [-f FILE] [-t TEST]
```



---

## Verbosity Modes


```text
-NORMAL
-SORT
-MINIMAL
-MINIMAL_NO_STACK
-SUPER_MINIMAL
default is NORMAL
```


---
* Options may be combined in any way.
---


## Test Discovery

The path is resolved relative to the current working directory.

A file is considered discoverable when:

* The file name begins with `test_`
* The file exists inside a directory named `tests`


## Filter Combination Behavior

Filters are applied from broadest to narrowest scope:

1. Discover tests within `-d` (if provided)
2. Restrict to `-f` (if provided)
3. Restrict to `-t` (if provided)
* If used alone, the entire project is searched.


```bash
python3 -m tini_test
```



### `-d DIRECTORY`

Limit test discovery to a specific directory.

```bash
tini_test -d test_math
```

All tests in the `test_math` will run.


---

### `-f FILE`

Limit execution to tests contained in a specific file.


```bash
python3 -m tini_test -f test_concurrency
python3 -m tini_test -f test_concurrency.py
```


notes:
If multiple files with same names exist in different directories all will run.


---

### `-t TEST`

Run a specific test function.


```bash
python3 -m tini_test -t function_name
```




notes:
If multiple functions with the same name are defined in different files only the first one spotted will run.

---



## Test Registration

```python
@Test.case
def test_example() -> None:
    ...

@Test.case()
def test_another_example() -> None:
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
```

### Flow

- Setup is executed before the test function runs.


- Cleanup is executed after the test function completes.

- Cleanup execution is still attempted when setup or test execution fails.

- Maybe further down the road this will be made optional by a flag.

---

### Catch exceptions

```python
@Test.case
def test_math() -> None:

    with WillRaise(NameError, ZeroDivisionError):   
        1/0
```
Notes: If one of the provided exceptions is not raised the test will fail and raise an `ExceptionWasNotRaised` exception.

### Compare variables

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

## Output Modes

### NORMAL

Displays:

* Test discovery information
* Setup execution
* Test execution
* Cleanup execution
* Full exception details
* Stack traces

If `print()` is called in any stage it will be displayed in order.

---

### SORT

Works the same way as normal. But failures are sorted to the bottom.

The sorting is only applied per module . 

Maybe further down the road we could implement a flag to sort globally.

---

### MINIMAL

Minimal display where:

* Failed tests are included ( names only )
* Associated stack traces
* Final execution summary




`MINIMAL_NO_STACK` is same as `MINIMAL`, except that no stack traces are shown.


`SUPER_MINIMAL` is same as `MINIMAL_NO_STACK` but less verbose.

---

### Misc

Comparing custom classes should try to autodiscover __eq__ and apply it althought 
, better to be explicit and pass the comperator tho ...

---

while the discovery implementation will find tests with the same names or sub dirs with same names or even actual tests cases with same names, it is heavily discouraged.

Of course the above is somewhat cancelled because the algorithm tries to autocomplete the path as a result when searching for a sub directory that exists in multiple sub directories with the same name no guarantess are made all tests will be excecuted.


---

## Roadmap

* [ ] Register tests into groups
* [ ] Support group-level setup executed once
* [ ] Support group-level cleanup execution
* [ ] Add global fail sort mode, not just per module.
