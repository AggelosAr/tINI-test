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
        {1, 2, 3, 4, 5, 6, 8},
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


@Test.case
@Shared(var.file_coverage)
def test_try_except_else_finally():
    case_code = textwrap.dedent('''
        try:                    # 1     l no. 1
            x = 1               # 2     l no. 2
        except ValueError:      # 3     l no. 3
            y = 2               # 4     l no. 4
        else:                   #       l no. 5
            z = 3               # 5     l no. 6
        finally:                #       l no. 7
            w = 4               # 6     l no. 8
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 6, 8},
        set(),
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

    status = var.file_coverage.categorize_python_statement(5)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(6)
    must_equal(LineStatus.RUN, status)


@Test.case
@Shared(var.file_coverage)
def test_try_except_multiple_handlers():
    case_code = textwrap.dedent('''
        try:                    # 1     l no. 1
            x = 1               # 2     l no. 2
        except ValueError:      # 3     l no. 3
            y = 2               # 4     l no. 4
        except KeyError:        # 5     l no. 5
            z = 3               # 6     l no. 6
        except:                 # 7     l no. 7
            w = 4               # 8     l no. 8
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 3, 4},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(4)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(5)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(6)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(7)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(8)
    must_equal(LineStatus.MISSING, status)


@Test.case
@Shared(var.file_coverage)
def test_for_loop_with_else():
    case_code = textwrap.dedent('''
        for i in range(3):      # 1     l no. 1
            x = i               # 2     l no. 2
        else:                   #       l no. 3
            y = 99              # 3     l no. 4
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 4},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.RUN, status)


    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.MISSING, status)


@Test.case
@Shared(var.file_coverage)
def test_while_loop_with_else():
    case_code = textwrap.dedent('''
        i = 0                   # 1     l no. 1
        while i < 3:            # 2     l no. 2
            i += 1              # 3     l no. 3
        else:                   #       l no. 4
            x = 99              # 4     l no. 5
    ''').strip()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(case_code)
        f.flush()
        temp_path = Path(f.name)
    
    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 3, 5},
        set(),
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(4)
    must_equal(LineStatus.RUN, status)


    var.file_coverage = FileCoverage(
        temp_path,
        {1, 2, 5},
        {3},
        False
    )
    var.file_coverage.parse_file()
    
    status = var.file_coverage.categorize_python_statement(1)
    must_equal(LineStatus.RUN, status)

    status = var.file_coverage.categorize_python_statement(2)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(3)
    must_equal(LineStatus.MISSING, status)

    status = var.file_coverage.categorize_python_statement(4)
    must_equal(LineStatus.RUN, status)
    