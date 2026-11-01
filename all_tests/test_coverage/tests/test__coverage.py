from itertools import cycle
from tini_test import Test
from tini_test.coverage._coverage import CoverageTracker, FileCoverage
import tempfile
import textwrap

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

    var_args(1, 0, 0, 1, 0, 0, 0, 0, 7)

    var.covered_lines = set([0, 1])
    _assert()
    
    var.covered_lines = set([1, 2])
    _assert()
    
    var.covered_lines = set([2, 12])
    _assert()

    var.covered_lines = set([12])
    _assert()

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
