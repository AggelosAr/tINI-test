from tini_test._internals.consts import _PROFILING
from tini_test.coverage._coverage import CoverageTracker

from ._internals._profiler import profiler
from .arg_parser import (CoreArgsDict, CoverageGenerateReportArgsDict,
                         CoverageMergeArgsDict, receive_args)
from .initializer import initialize_test_suite
from .misc.exceptions import CantFindRelativePathToRoot


@profiler(_PROFILING)
def _tini_test(kwargs: CoreArgsDict | CoverageMergeArgsDict | CoverageGenerateReportArgsDict):

    if 'merge_directory' in kwargs:
        CoverageTracker.merge(**kwargs)

    elif 'store' in kwargs:
        CoverageTracker.init_from_store(**kwargs).to_html()
    
    else:
        try:
            test_suite = initialize_test_suite(**kwargs)
            
        except CantFindRelativePathToRoot:
            raise

        else:
            test_suite.runner()
            test_suite.pprint()


        test_suite.get_coverage()


if __name__=='__main__':
    
    _tini_test(receive_args())
