from tini_test._internals.consts import _PROFILING
from tini_test.coverage._coverage import CoverageTracker
from tini_test.enums import TiniTestMode

from ._internals._profiler import profiler
from .arg_parser import (CoreArgsDict, CoverageGenerateReportArgsDict,
                         CoverageMergeArgsDict, receive_args)
from .initializer import initialize_test_suite
from .misc.exceptions import CantFindRelativePathToRoot


@profiler(_PROFILING)
def _tini_test(kwargs: CoreArgsDict 
                        | CoverageMergeArgsDict 
                        | CoverageGenerateReportArgsDict,
               mode: TiniTestMode):
    
    match mode:

        case TiniTestMode.MERGE:
            CoverageTracker.merge(**kwargs)

        case TiniTestMode.HTML_REPORT:
            CoverageTracker.init_from_store(**kwargs).to_html()

        case TiniTestMode.RUN:
            try:
                test_suite = initialize_test_suite(**kwargs)
                
            except CantFindRelativePathToRoot:
                raise

            else:
                test_suite.runner()
                test_suite.pprint()

            test_suite.get_coverage()


if __name__=='__main__':
    _tini_test(*receive_args())
