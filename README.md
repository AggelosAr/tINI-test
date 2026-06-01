# Small Test

A lightweight Python test framework focused on simple test discovery and execution from the command line.

## Usage

```bash
small_test [VERBOSITY] [-d DIRECTORY | -f FILE] [-t TEST]
```

### Verbosity Modes

One verbosity mode may be specified:

```text
-NORMAL
-SORT
-MINIMAL
-MINIMAL_NO_STACK
```

If no verbosity mode is provided, `NORMAL` is used.

| Mode             | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| NORMAL           | Full execution flow, detailed output, and stack traces.         |
| SORT             | Results are displayed in sorted order with failures shown last. |
| MINIMAL          | Only failed tests and their stack traces are displayed.         |
| MINIMAL_NO_STACK | Same as MINIMAL, but stack traces are suppressed.               |

## Search Options

### `-d DIRECTORY`

Run all discovered tests within a directory.

The directory path is resolved relative to the current terminal working directory.

Example:

```bash
small_test -NORMAL -d src/test_folder
```

Notes:

* All discovered tests under the target directory are executed.
* If multiple nested directories share the same name, only the first matching directory found will be collected.

### `-f FILE`

Run all tests contained in a specific test file.

The framework searches the entire project for the file.

The file may be provided with or without the `.py` extension.

Example:

```bash
small_test -SORT -f test_concurrency
```

Notes:

* All tests inside the matching file are executed.
* If multiple files with the same name exist, only the first match is used.

### `-t TEST`

Run a specific test function.

Example:

```bash
small_test -MINIMAL -t testing_something
```

Behavior:

* If neither `-d` nor `-f` is specified, the framework searches the entire project for the test function.
* If `-d` or `-f` is specified, the search is limited to the discovered test files within that scope.
* If multiple matching test files exist, only the first matching file is used.

Example:

```python
def testing_something(*args, **kwargs):
    ...
```

Run:

```bash
small_test -t testing_something
```

## Default Behavior

If no search option is provided, the framework discovers and executes all tests within the current directory.

```bash
small_test
```

## Test Discovery

A test file is considered discoverable when:

* The file name begins with `test_`
* The file is a Python file (`.py`)
* The file resides somewhere under a directory named `tests`

Example:

```text
project/
└── tests/
    ├── test_math.py
    └── test_concurrency.py
```

## Test Registration

Tests are collected from functions decorated with the Small Test decorator.

```python
@small_test(...)
def test_example():
    ...
```

The decorator accepts up to two optional arguments:

```python
@small_test(setup, cleanup)
```

Both arguments must be callables (typically lambdas).

### Setup

Executed before the test function runs.

### Cleanup

Executed after the test completes.

If the setup or the test itself fails, an attempt will still be made to execute the cleanup function.

## Output Modes

### NORMAL

Displays:

* Test discovery information
* Setup execution
* Test execution
* Cleanup execution
* Full exception details
* Stack traces

Print statements executed within tests are displayed.

### SORT

Same behavior as NORMAL, but results are grouped and sorted.

Failures are displayed after successful tests.

Print statements executed within tests are displayed.

### MINIMAL

Displays:

* Only failed tests
* Stack traces for failures

### MINIMAL_NO_STACK

Displays:

* Only failed tests
* No stack traces

## Example Commands

Run all tests under a directory:

```bash
small_test -NORMAL -d src/test_folder
```

Run all tests in a file:

```bash
small_test -SORT -f test_concurrency
```

Run a specific test:

```bash
small_test -MINIMAL -t function_that_tests_something
```

## Framework Validation

The framework has been tested using its own test suite.

## Roadmap


### Coverage

* [ ] Calculate test coverage


### Output Improvements

* [ ] Add separators to MINIMAL stack traces
* [ ] Add start separators in NORMAL and SORT modes
* [ ] Add final execution summary


### Test Execution

* [ ] Improve SORT mode by grouping failures by category


### Groups

* [ ] Register tests into groups
* [ ] Support group-level setup executed once
* [ ] Support group-level cleanup execution


### Configuration

* [ ] Support configurable colors
* [ ] Support configurable output formatting


### Misc

* [ ] Make correctly failing tests pass.
* [ ] test must equal on cleanup and breakup ? 
* [ ] remove capturing of std out in case of MINIMAL modes etc or a flag ... currently everything is captured always
