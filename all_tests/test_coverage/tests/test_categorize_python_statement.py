import tempfile
import textwrap
from pathlib import Path

from tini_test import Test
from tini_test.coverage._coverage import FileCoverage
from tini_test.coverage.enums import LineStatus
from tini_test.must_equals import must_equal
from tini_test.shared import Shared, var


@Test.case
@Shared(var.file_coverage)
def test_leaf_statement_single_pass():
    case_code = textwrap.dedent('''
        x = 1
        y = 2
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    # Line 1 ran successfully
    var.file_coverage = FileCoverage(
        temp_path,
        {1},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.MISSING, status)


@Test.case
@Shared(var.file_coverage)
def test_leaf_statement_no_pass():
    case_code = textwrap.dedent('''
        x = 1
        y = 2
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        set(),
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.MISSING, status)


@Test.case
@Shared(var.file_coverage)
def test_multi_line_statement():
    case_code = textwrap.dedent('''
        x = (
            1 +
            2
        )
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    # Some lines ran, some failed (multi-line statement edge case)
    var.file_coverage = FileCoverage(
        temp_path,
        {1},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)


@Test.case
@Shared(var.file_coverage)
def test_compound_statement():
    case_code = textwrap.dedent('''
        if x > 0:  # 1
            y = 1  # 2 
            z = 2  # 3 X
        else:      # 
            w = 3  # 4
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {2},
        {3},
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(4)
    must_equal(LineStatus.MISSING, status)




@Test.case
@Shared(var.file_coverage)
def test_compound_statement_with_function():
    case_code = textwrap.dedent('''
        def foo(x):             # 1     l no. 1
            if 1:               # 2     l no. 2
                return 1/0      # 3     l no. 3
            else:               #       l no. 4
                return 0        # 4     l no. 5
                                #       l no. 6
        foo(1)                  # 5     l no. 7
        foo(2)                  # 6     l no. 8
        
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 3, 4, 5, 6, 7, 8},
        {3},
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(4)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(5)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(6)
    must_equal(LineStatus.RUN, status)
