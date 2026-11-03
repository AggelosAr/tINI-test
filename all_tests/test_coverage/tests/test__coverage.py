import tempfile
import textwrap
from itertools import cycle
from pathlib import Path

from tini_test import Test
from tini_test.coverage._coverage import (CoverageTracker, FileCoverage,
                                          InlineComment, Line)
from tini_test.coverage.enums import LineStatus
from tini_test.must_equals import must_equal
from tini_test.shared import Shared, var

# Partial on shared in not supported?
# Shared = partial(Shared, var.coverage, var.case, var.covered_lines, var.args)

# Var has no autocomplete
minn = True

def short_summary() -> None:

    _titles = ('Statements', 
               'Run',
               'Correctly Missing', 
               'Missing', 
               'Incorrectly Run',
               'Excluded', 
               'Comment',
               'Docstring',
               'Empty')


    max_titles = max(len(title) for title in _titles)
    max_digits = max(len(str(var.coverage.total_statements)), 
                     len(str(var.coverage.covered_statements)),
                     len(str(var.coverage._X_correctly_missing_statements)),
                     len(str(var.coverage.missing_statements)),
                     len(str(var.coverage._X_incorrectly_covered_statements)), 
                     len(str(var.coverage.excluded_statements)), 
                     len(str(var.coverage.comment_lines)),
                     len(str(var.coverage.docstring_lines)),
                     len(str(var.coverage.empty_lines)),
                     len('100.0'))
    _max = max(max_titles, max_digits)

    if minn:
        for idx, line in enumerate(var.case.splitlines()):
            print('%d: %s' % (idx + 1, line))

        print('\nRUNTIME COVERED LINES: ', var.covered_lines)

        print(
            '\n\n              '  \
            'Coverage Summary\n'  \
            '----------------\n'  \
            '%s\n'                \
            '\n'                  \
            '%s\n\n\n'            \
                % 
                (
                    '  '.join(map(CoverageTracker.pad, _titles, [_max]*len(_titles))),
                    '  '.join([
                        CoverageTracker.pad(var.coverage.total_statements, _max), 
                        CoverageTracker.pad(var.coverage.covered_statements, _max), 
                        CoverageTracker.pad(var.coverage._X_correctly_missing_statements, _max), 
                        CoverageTracker.pad(var.coverage.missing_statements, _max), 
                        CoverageTracker.pad(var.coverage._X_incorrectly_covered_statements, _max), 
                        CoverageTracker.pad(var.coverage.excluded_statements, _max), 
                        CoverageTracker.pad(var.coverage.comment_lines, _max), 
                        CoverageTracker.pad(var.coverage.docstring_lines, _max), 
                        CoverageTracker.pad(var.coverage.empty_lines, _max),
                    ])
                )
        )


    
def from_file_coverage():
    
    with tempfile.NamedTemporaryFile('w+') as f:
        f.write(textwrap.dedent(var.case))
        f.flush()

        coverage = FileCoverage(f.name, var.covered_lines, False)
        coverage.parse_file()
     
    var.coverage = coverage


def _assert():
    if minn:
        print('------------------')

    from_file_coverage()
    
    if minn:
        print('------------------')
        short_summary()

    must_equal(next(var.args), var.coverage.total_statements)
    must_equal(next(var.args), var.coverage.covered_statements)
    must_equal(next(var.args), var.coverage._X_correctly_missing_statements)
    must_equal(next(var.args), var.coverage.missing_statements)
    must_equal(next(var.args), var.coverage._X_incorrectly_covered_statements)
    must_equal(next(var.args), var.coverage.excluded_statements)
    must_equal(next(var.args), var.coverage.comment_lines)
    must_equal(next(var.args), var.coverage.docstring_lines)
    must_equal(next(var.args), var.coverage.empty_lines)


def var_args(*args):
    var.args = cycle(args)



@Test.case
@Shared(var.coverage, var.case, var.covered_lines, var.args)
def test_continuation_block():
    var.case = r'''

A = (

    'A', 

    'B',

    'C' 

)

'''
    # Autocomplete is on TODO add test with mocking on fails
    var_args(1, 1, 0, 0, 0, 0, 0, 0, 7)

    var.covered_lines = set([0, 1])
    _assert()

    var_args(1, 0, 0, 1, 0, 0, 0, 0, 7)
    var.covered_lines = set([1, 2])
    _assert()

    var_args(1, 0, 0, 1, 0, 0, 0, 0, 7)
    var.covered_lines = set([2, 12])
    _assert()

    var_args(1, 0, 0, 1, 0, 0, 0, 0, 7)
    var.covered_lines = set([12])
    _assert()

    var_args(1, 1, 0, 0, 0, 0, 0, 0, 7)
    var.covered_lines = set([0, 1, 2, 12])
    _assert()
    




@Test.case
@Shared(var.coverage, var.case, var.covered_lines, var.args)
def test_continuation_block_passes():
    var.case = r'''


A = (

    'A', 

     'B',

      'C' 

    
)


'''
    var_args(1, 1, 0, 0, 0, 0, 0, 0, 10)

    var.covered_lines = set([4, ])
    _assert()
    
    var.covered_lines = set([4, 6, 8])
    _assert()

    var.covered_lines = set([5, 7, 9])
    _assert()

    var.covered_lines = set([6, 8, 10])
    _assert()

    var.covered_lines = set([7, 9, 11])
    _assert()
    
    var.covered_lines = set([8, 10, 13])
    _assert()

    var.covered_lines = set([9, 11, 4])
    _assert()

    var.covered_lines = set([10, 12, 7])
    _assert()

    var.covered_lines = set([11, 4, 10])
    _assert()

    var.covered_lines = set([12, 5, 7])
    _assert()

    var.covered_lines = set([13, 6, 9])
    _assert()



@Test.case
@Shared(var.coverage, var.case, var.covered_lines, var.args, var.rargs)
def test_continuation_block_with_assert_not_covered():
    def run():
        var_args(*var.rargs)
        
        var.covered_lines = set([3, ])
        _assert()

        var.covered_lines = set([4, ])
        _assert()

        var.covered_lines = set([5, ])
        _assert()

        var.covered_lines = set([6, ])
        _assert()

        var.covered_lines = set([7, ])
        _assert()

        var.covered_lines = set([8, ])
        _assert()

        var.covered_lines = set([9, ])
        _assert()

        var.covered_lines = set([10, ])
        _assert()

        var.covered_lines = set([11, ])
        _assert()


    var.case = '''

    A = (           # >>> assert missing

        'A', 

        'B',

        'C' 

    )
    
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 7
    run()

    
    var.case = '''
    
    A = (           
                    # >>> assert missing
        'A', 
    
        'B',
    
        'C' 
    
    )
      
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 6
    run()

    var.case = '''
    
    A = (           
    
        'A',        # >>> assert missing
    
        'B',
    
        'C' 
    
    )
      
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 7
    run()

    var.case = '''
    
    A = (           
    
        'A',
                    # >>> assert missing
        'B',
    
        'C' 
    
    )
      
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 6
    run()

    var.case = '''
    
    A = (   
    
        'A', 
    
        'B',        # >>> assert missing
    
        'C' 
    
    )
      
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 7
    run()

    var.case = '''
    
    A = (           
    
        'A', 
    
        'B',
                    # >>> assert missing
        'C' 
    
    )
      
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 6
    run()

    var.case = '''
        
    A = (           
    
        'A', 
    
        'B',
                
        'C'         # >>> assert missing
    
    )
        
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 7
    run()

    var.case = '''
            
    A = (           
    
        'A', 
    
        'B',
                
        'C'         
                    # >>> assert missing
    )
        
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 6
    run()

    var.case = '''
                
    A = (           
    
        'A', 
    
        'B',
                
        'C'         
                    
    )               # >>> assert missing
        
    '''
    var.rargs = 1, 0, 0, 0, 1, 0, 1, 0, 7
    run()


    var.case = '''
                    
    A = (           
    
        'A', 
    
        'B',
                
        'C'         
                    
    )               



    A = (           
        
            'A', 
        
            'B',
                    
            'C'         
                        
    )               # >>> assert missing
        
    '''
    var.rargs = 2, 1, 1, 0, 0, 0, 1, 0, 14
    run()


    

@Test.case
@Shared(var.coverage, var.case, var.covered_lines, var.args, var.rargs)
def test_comments_docstrings():

    var.case = '''
    # comment                        
    A = (           # comment
                    # comment
        'A',        # comment
                    # comment
        'B',        # comment
                    # comment
        'C'         # comment
                    # comment
    )               # comment
    # comment    
    '''

    var.covered_lines = set([2])

    from_file_coverage()
    # short_summary()
    must_equal(1,  var.coverage.total_statements)
    must_equal(0,  var.coverage.covered_statements)
    must_equal(0,  var.coverage._X_correctly_missing_statements)
    must_equal(1,  var.coverage.missing_statements)
    must_equal(0,  var.coverage._X_incorrectly_covered_statements)
    must_equal(0,  var.coverage.excluded_statements)
    must_equal(11, var.coverage.comment_lines)
    must_equal(0,  var.coverage.docstring_lines)
    must_equal(1,  var.coverage.empty_lines)


    var.case = r'''
    %s # comment
    """""" # comment
    A = (           # comment
                    # comment
        'A',        # comment
                    # comment
        'B',        # comment
                    # comment
        'C'         # comment
                    # comment
    )               
                    
    """""" # comment
    """""" # comment
    """""" # comment
    """""" # comment
    """""" # comment
    A = (           # comment
                    # comment
            'A',    # comment
                    # comment
            'B',    # comment
                    # comment
            'C'     # comment
                    # comment    
    )               
                    
    """""" # comment ^^ this is not allowed
    """""" # comment
    """""" # comment
    """""" # comment
    ''' % "''''''"
    var.covered_lines = set([3])

    from_file_coverage()
    # short_summary()

    must_equal(2,  var.coverage.total_statements)
    must_equal(0,  var.coverage.covered_statements)
    must_equal(0,  var.coverage._X_correctly_missing_statements)
    must_equal(2,  var.coverage.missing_statements)
    must_equal(0,  var.coverage._X_incorrectly_covered_statements)
    must_equal(0,  var.coverage.excluded_statements)
    must_equal(27, var.coverage.comment_lines)
    must_equal(11, var.coverage.docstring_lines)
    must_equal(3,  var.coverage.empty_lines)


    '''#
    '''#
    var.case = r'''
                       
    A = (           
                    
        'A',       
                   
        'B',       
                    
        'C'        
                  
    )              
    
    x = 10

    %s         # comment ?
    Docstring   # comment ?
                # comment ?
    %s         # comment

    """         # comment ?
                # comment ?
    Docstring   # comment ?
    """         # comment
    ''' % ("'''", "'''")


     # >>> assert missing

    var.covered_lines = set([3])
    
    from_file_coverage()
    # short_summary()

    must_equal(2,  var.coverage.total_statements)
    must_equal(1,  var.coverage.covered_statements)
    must_equal(0,  var.coverage._X_correctly_missing_statements)
    must_equal(1,  var.coverage.missing_statements)
    must_equal(0,  var.coverage._X_incorrectly_covered_statements)
    must_equal(0,  var.coverage.excluded_statements)
    must_equal(2,  var.coverage.comment_lines)
    must_equal(2,  var.coverage.docstring_lines)
    must_equal(9,  var.coverage.empty_lines)
    


    var.case = '''
    def example():
        """Function docstring."""

        x = 10

        """
        Some random multiline string.
        """

        if x:
            """Another string."""

    class Example:
        """Class docstring."""
    '''

    var.covered_lines = set([])
    
    from_file_coverage()
    # short_summary()

    must_equal(4,  var.coverage.total_statements)
    must_equal(0,  var.coverage.covered_statements)
    must_equal(0,  var.coverage._X_correctly_missing_statements)
    must_equal(4,  var.coverage.missing_statements)
    must_equal(0,  var.coverage._X_incorrectly_covered_statements)
    must_equal(0,  var.coverage.excluded_statements)
    must_equal(0,  var.coverage.comment_lines)
    must_equal(4,  var.coverage.docstring_lines)
    must_equal(5,  var.coverage.empty_lines)


@Test.case
def test_inline_comment_assert_not_covered():
    line = 'value = 1  # >>> assert missing'
    marker = InlineComment(line.index('#'))
    must_equal(True, InlineComment.assert_not_covered(line, marker))

    no_comment_line = 'value = 1'
    must_equal(False, InlineComment.assert_not_covered(no_comment_line, None))

    other_line = 'value = 1  # ordinary comment'
    other_comment = InlineComment(other_line.index('#'))

    must_equal(False, InlineComment.assert_not_covered(other_line, other_comment))


@Test.case
def test_line_get_split_line():
    line_content = 'value = 1  # note'
    line = Line(1, 
                line_content, 
                LineStatus.RUN,
                inline_comment=InlineComment(line_content.index('#')))

    must_equal(('value = 1  ', '# note'), line.get_split_line())

    no_comment_line = 'value = 1'
    line = Line(1, no_comment_line, LineStatus.RUN)
    must_equal(('value = 1', ''), line.get_split_line())


@Test.case
def test_line_is_else_or_finally():
    must_equal(True, Line(1, 'else:', LineStatus.RUN).is_else_or_finally)
    must_equal(True, Line(1, 'finally:', LineStatus.RUN).is_else_or_finally)
    must_equal(False, Line(1, 'elsewhere:', LineStatus.RUN).is_else_or_finally)


@Test.case
def test_file_coverage_handle_ellipsis():
    covered = FileCoverage(Path('unused.py'), {1}, False)
    covered.source = '...  # note'
    covered._statement_counts[LineStatus.RUN] = 1
    covered_line = Line(1, '...  # note', LineStatus.RUN)
    covered.handle_ellipsis(covered_line)

    must_equal(LineStatus.EXCLUDED, covered_line.status)
    must_equal(0, covered.covered_statements)
    must_equal(1, covered.excluded_statements)
    must_equal(1, covered.comment_lines)
    must_equal(True, covered_line.is_inline_commented)

    missing = FileCoverage(Path('unused.py'), set(), False)
    missing.source = '...'
    missing._statement_counts[LineStatus.MISSING] = 1
    missing_line = Line(1, '...', LineStatus.MISSING)
    missing.handle_ellipsis(missing_line)

    must_equal(LineStatus.EXCLUDED, missing_line.status)
    must_equal(0, missing.missing_statements)
    must_equal(1, missing.excluded_statements)
    must_equal(0, missing.comment_lines)


@Test.case
def test_test_suite_flow_get_coverage():
    from tini_test.core import TestSuite
    from tini_test.enums import Coverage, RunMode, Verbosity
    from tini_test.integrations.server import ServerManager

    class RecordingCoverageTracker(CoverageTracker):
        def __init__(self):
            super().__init__(None)
            self.calls = []

        def reconcile(self):
            self.calls.append('reconcile')

        def show_short_summary(self, long=False):
            self.calls.append(('show_short_summary', long))

        def serialize(self, reconcile=False):
            self.calls.append(('serialize', reconcile))

    def make_suite(coverage_mode, server_command):
        tracker = RecordingCoverageTracker()
        suite = TestSuite(
            root='.',
            run_mode=RunMode.SYNC,
            verbosity=Verbosity.NORMAL,
            coverage=coverage_mode,
            coverage_tracker=tracker,
            server=ServerManager(server_command, None, None),
        )
        return suite, tracker

    suite, tracker = make_suite(Coverage.DISABLED, None)
    suite.get_coverage()
    must_equal([], tracker.calls)

    suite, tracker = make_suite(Coverage.ENABLED, None)
    suite.get_coverage()
    must_equal(
        [('show_short_summary', False), ('serialize', False)],
        tracker.calls,
    )

    suite, tracker = make_suite(Coverage.ENABLED, 'unused server command')
    suite.get_coverage()
    must_equal(
        ['reconcile', ('show_short_summary', False), ('serialize', False)],
        tracker.calls,
    )
