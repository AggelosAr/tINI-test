# tINI test

A lightweight Python test framework focused on simple test discovery and execution from the command line.

## Usage

```bash
tini_test [VERBOSITY] [-d DIRECTORY] [-f FILE] [-t TEST]
```

Search options may be combined in any way.

```bash
src/
├── testing_async/
│   ├── tests/
│   │   ├── test_concurrency.py
│   │   └── test_x.py
├── testing_sync/
│       └── testing_dir/
│           └── tests/
│               ├── test_concurrency.py
│               └── test_y.py
```


If no verbosity mode is specified, `NORMAL` is used. ???

---

## Verbosity Modes

Verbosity mode may be specified:

```text
-NORMAL
-SORT
-MINIMAL
-MINIMAL_NO_STACK
-SUPER_MINIMAL
```


---




## Test Discovery

The directory path is resolved relative to the current working directory.

A file is considered discoverable when:

* The file name begins with `test_`
* The file has a `.py` extension
* The file exists inside a directory named `tests`

while the discovery implementation will find tests with the same names or sub dirs with same names or even actual tests cases with same names, it is heavily discouraged.

Of course the above is somewhat cancelled because the algorithm tries to autocomplete the path as a result when searching for a sub directory that exists in multiple sub directories with the same name no guarantess are made all tests will be excecuted.


## Filter Combination Behavior

Filters are applied from broadest to narrowest scope:

1. Discover tests within `-d` (if provided)
2. Restrict to `-f` (if provided)
3. Restrict to `-t` (if provided)

* If used alone, the entire project is searched.



## Default Behavior

If no search option is supplied, all discoverable tests under the current directory are executed.

```bash
python3 -m tini_test
```



### `-d DIRECTORY`

Limit test discovery to a specific directory.

```bash
tini_test -d testing_dir
```

All tests in the `testing_dir` will run.


---

### `-f FILE`

Limit execution to tests contained in a specific file.

The file may be supplied with or without the `.py` extension.



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




```bash
python3 -m tini_test -d test_math/tests
or 
python3 -m tini_test -d test_math/
```

Runs all tests inside `test_math/tests`.


```bash
python3 -m tini_test -d test_math -f test_concurrency
```

Runs all tests inside `test_concurrency.py` located within `test_math`.

```bash
python3 -m tini_test -d test_math -f test_concurrency -t test_addition
```

Runs only `test_addition` from `test_concurrency.py` within `test_math`.

---



## Test Registration

Tests are registered using the Small Test decorator.

```python
@tini_test()
def test_example():
    ...
```

The decorator accepts up to two optional callables:

```python
@tini_test(setup, cleanup)
```

Example:

```python
@tini_test(
    lambda: create_database(),
    lambda: destroy_database()
)
def test_database():
    ...
```

### Setup

Executed before the test function runs.

### Cleanup

Executed after the test function completes.

Cleanup execution is still attempted when setup or test execution fails.

maybe further down the road this will be made optional by a flag 

---

## Output Modes

### NORMAL

Displays:

* Test discovery information
* Setup execution
* Test execution
* Cleanup execution
* Full exception details
* Stack traces

If `print()` is called in any stage it will displayed in order.

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
---

### MINIMAL_NO_STACK


Same as minimal 

Except that No stack traces are shown


---

### SUPER_MINIMAL

Same as MINIMAL_NO_STACK but less verbose.
---



---


Comparing custom classes should try to autodiscover __eq__ and apply it althought 
, better to be explicit and pass the comperator tho ...





## Framework Validation

The framework is tested using its own test suite.

---

## Roadmap

### Coverage

* [ ] Calculate test coverage


### Groups

* [ ] Register tests into groups
* [ ] Support group-level setup executed once
* [ ] Support group-level cleanup execution


### Configuration

* [ ] Support configurable


### Misc

FIX failing tests

ADD SUPER SORT mode to sort All failures and show them last, not just sort failures on bottom per module.
* [ ] remove capturing of std out in case of MINIMAL modes etc or a flag ... currently everything is captured always
