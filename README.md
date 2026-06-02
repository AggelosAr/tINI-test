# Small Test

A lightweight Python test framework focused on simple test discovery and execution from the command line.

## Usage

```bash
small_test [VERBOSITY] [-d DIRECTORY] [-f FILE] [-t TEST]
```

Search options may be combined in any way.

Examples:

```bash
small_test -d tests
small_test -f test_math
small_test -t test_addition

small_test -d tests -t test_addition
small_test -f test_math -t test_addition
small_test -d tests -f test_math -t test_addition
```

If no verbosity mode is specified, `NORMAL` is used.

---

## Verbosity Modes

One verbosity mode may be specified:

```text
-NORMAL
-SORT
-MINIMAL
-MINIMAL_NO_STACK
-SUPER_MINIMAL
```

| Mode             | Description                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| NORMAL           | Full execution flow, detailed output, and stack traces.                                            |
| SORT             | Same as NORMAL, but results are sorted with failures shown last.                                   |
| MINIMAL          | Only failed tests and their stack traces are displayed.                                            |
| MINIMAL_NO_STACK | Only failed tests are displayed. Stack traces are suppressed.                                      |
| SUPER_MINIMAL    | Displays only final summary statistics. No failures, stack traces, or execution details are shown. |

---

## Search Options

Search options act as filters.

### `-d DIRECTORY`

Limit test discovery to a specific directory.

The directory path is resolved relative to the current working directory.

Example:

```bash
small_test -d src/tests
```

Notes:

* All discoverable tests under the directory are collected.
* If multiple directories share the same name, only the first match is used.

---

### `-f FILE`

Limit execution to tests contained in a specific file.

The file may be supplied with or without the `.py` extension.

Example:

```bash
small_test -f test_concurrency
```

Notes:

* All tests within the matching file are executed.
* If multiple files share the same name, only the first match is used.

---

### `-t TEST`

Run a specific test function.

Example:

```bash
small_test -t test_something
```

Example test:

```python
@small_test()
def test_something():
    ...
```

Notes:

* If used alone, the entire project is searched.
* If combined with `-d`, searching is limited to that directory.
* If combined with `-f`, searching is limited to that file.
* If multiple matching tests are discovered, only the first match is executed.

---

## Filter Combination Behavior

Filters are applied from broadest to narrowest scope:

1. Discover tests within `-d` (if provided)
2. Restrict to `-f` (if provided)
3. Restrict to `-t` (if provided)

Examples:

```bash
small_test -d tests
```

Runs all discovered tests under `tests`.

```bash
small_test -f test_math
```

Runs all tests inside `test_math.py`.

```bash
small_test -d tests -f test_math
```

Runs all tests inside `test_math.py` located within `tests`.

```bash
small_test -d tests -f test_math -t test_addition
```

Runs only `test_addition` from `test_math.py` within `tests`.

---

## Default Behavior

If no search option is supplied, all discoverable tests under the current directory are executed.

```bash
small_test
```

---

## Test Discovery

A file is considered discoverable when:

* The file name begins with `test_`
* The file has a `.py` extension
* The file exists somewhere beneath a directory named `tests`

Example:

```text
project/
└── tests/
    ├── test_math.py
    └── test_concurrency.py
```

---

## Test Registration

Tests are registered using the Small Test decorator.

```python
@small_test()
def test_example():
    ...
```

The decorator accepts up to two optional callables:

```python
@small_test(setup, cleanup)
```

Example:

```python
@small_test(
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

Output written with `print()` is displayed.

---

### SORT

Displays the same information as NORMAL.

Results are sorted with failed tests displayed after successful tests.

Output written with `print()` is displayed.

---

### MINIMAL

Displays:

* Failed tests only
* Associated stack traces

---

### MINIMAL_NO_STACK

Displays:

* Failed tests only
* No stack traces

---

### SUPER_MINIMAL

Displays:

* Final execution summary only

No test output, stack traces, setup information, cleanup information, or failure details are shown.

---

## Example Commands

Run all tests:

```bash
small_test
```

Run all tests under a directory:

```bash
small_test -NORMAL -d tests
```

Run all tests in a file:

```bash
small_test -SORT -f test_concurrency
```

Run a single test:

```bash
small_test -MINIMAL -t test_addition
```

Run a specific test from a specific file:

```bash
small_test -f test_math -t test_addition
```

Run a specific test from a file within a directory:

```bash
small_test -d tests -f test_math -t test_addition
```

---

## Framework Validation

The framework is tested using its own test suite.

---

## Roadmap

### Coverage

* [ ] Calculate test coverage


### Output Improvements

* [ ] Add separators to MINIMAL stack traces
* [ ] Add start separators in NORMAL and SORT modes


### Groups

* [ ] Register tests into groups
* [ ] Support group-level setup executed once
* [ ] Support group-level cleanup execution


### Configuration

* [ ] Support configurable


### Misc

* [ ] Make correctly failing tests pass.
* [ ] test must equal on cleanup and breakup ? 
* [ ] remove capturing of std out in case of MINIMAL modes etc or a flag ... currently everything is captured always
