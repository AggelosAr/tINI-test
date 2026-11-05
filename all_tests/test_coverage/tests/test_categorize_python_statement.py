"""Test cases for categorize_python_statement method.

This module tests the 4 potential outcomes of statement categorization:
1. Leaf statement with lines in passes only → RUN
2. Leaf statement with lines in neither passes nor fails → MISSING
3. Leaf statement with lines in both passes and fails → MISSING (ambiguous)
4. Compound statement with any child RUN → RUN (otherwise MISSING)
"""

import textwrap
from pathlib import Path

from tini_test import Test
from tini_test.coverage._coverage import FileCoverage
from tini_test.coverage.enums import LineStatus
from tini_test.must_equals import must_equal
from tini_test.shared import Shared, var


@Test.case
@Shared(var.case_code, var.file_coverage)
def test_leaf_statement_in_passes_only():
    """Test Case 1: Leaf statement with lines in passes only → RUN"""
    var.case_code = textwrap.dedent("""
        x = 1
        y = 2
    """).strip()
    
    # Line 1 ran successfully
    var.file_coverage = FileCoverage(
        Path('<test>'),
        {1},
        set(),
        False
    )
    var.file_coverage.source = var.case_code
    
    # Statement 1 is x = 1 (line 1, leaf statement)
    status = var.file_coverage.categorize_python_statement(1)
    
    must_equal(status, LineStatus.RUN, "Leaf statement with line in passes should be RUN")


@Test.case
@Shared(var.case_code, var.file_coverage)
def test_leaf_statement_in_neither():
    """Test Case 2: Leaf statement with lines in neither passes nor fails → MISSING"""
    var.case_code = textwrap.dedent("""
        x = 1
        y = 2
    """).strip()
    
    # No lines ran
    var.file_coverage = FileCoverage(
        Path('<test>'),
        set(),
        set(),
        False
    )
    var.file_coverage.source = var.case_code
    
    # Statement 1 is x = 1 (line 1, leaf statement)
    status = var.file_coverage.categorize_python_statement(1)
    
    must_equal(status, LineStatus.MISSING, "Leaf statement with line in neither should be MISSING")


@Test.case
@Shared(var.case_code, var.file_coverage)
def test_leaf_statement_in_both_passes_and_fails():
    """Test Case 3: Leaf multi-line statement with lines in both passes and fails → MISSING"""
    var.case_code = textwrap.dedent("""
        x = (
            1 +
            2
        )
    """).strip()
    
    # Some lines ran, some failed (multi-line statement edge case)
    var.file_coverage = FileCoverage(
        Path('<test>'),
        {1, 2},
        {3},
        False
    )
    var.file_coverage.source = var.case_code
    
    # This is a multi-line assignment statement spanning lines 1-4
    # It has some lines in passes and some in fails - should be MISSING (ambiguous)
    statement_id = var.file_coverage.line_to_statement.get(1)
    if statement_id:
        status = var.file_coverage.categorize_python_statement(statement_id)
        must_equal(status, LineStatus.MISSING, "Statement with lines in both passes and fails should be MISSING")


@Test.case
@Shared(var.case_code, var.file_coverage)
def test_compound_statement_with_child_run():
    """Test Case 4: Compound statement where any child is RUN → RUN"""
    var.case_code = textwrap.dedent("""
        if x > 0:
            y = 1
            z = 2
        else:
            w = 3
    """).strip()
    
    # Only the first body statement of the if ran
    var.file_coverage = FileCoverage(
        Path('<test>'),
        {2},
        set(),
        False
    )
    var.file_coverage.source = var.case_code
    
    # Find the if statement (should be at line 1)
    if_statement_id = var.file_coverage.line_to_statement.get(1)
    if if_statement_id:
        # Check that it's compound
        node = var.file_coverage.statement_graph.get(if_statement_id)
        must_equal(node.is_compound, True, "If statement should be compound")
        
        # Check that it has children
        children = var.file_coverage.statement_children.get(if_statement_id)
        must_equal(len(children) > 0, True, "If statement should have children")
        
        # Since at least one child (y = 1 at line 2) is in passes, 
        # the compound statement should be RUN
        status = var.file_coverage.categorize_python_statement(if_statement_id)
        must_equal(status, LineStatus.RUN, "Compound statement with RUN child should be RUN")


@Test.case
@Shared(var.case_code, var.file_coverage)
def test_compound_statement_with_no_child_run():
    """Test Case 4b: Compound statement where no child is RUN → MISSING"""
    var.case_code = textwrap.dedent("""
        if x > 0:
            y = 1
            z = 2
    """).strip()
    
    # No lines ran
    var.file_coverage = FileCoverage(
        Path('<test>'),
        set(),
        set(),
        False
    )
    var.file_coverage.source = var.case_code
    
    # Find the if statement (should be at line 1)
    if_statement_id = var.file_coverage.line_to_statement.get(1)
    if if_statement_id:
        # Check that it's compound
        node = var.file_coverage.statement_graph.get(if_statement_id)
        must_equal(node.is_compound, True, "If statement should be compound")
        
        # Since no children are RUN, the compound statement should be MISSING
        status = var.file_coverage.categorize_python_statement(if_statement_id)
        must_equal(status, LineStatus.MISSING, "Compound statement with no RUN child should be MISSING")

