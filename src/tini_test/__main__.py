from tini_test._internals.consts import _PROFILING
from tini_test.coverage._coverage import CoverageTracker
from tini_test.enums import TiniTestMode
from tini_test.integrations.server import ServerManager

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

                # command='python manage.py runserver --settings main.test_settings 127.0.0.1:8000 --noreload'
                # health_url='http://127.0.0.1:8000/'
                # server = ServerManager(command=command, health_url=health_url)

                # server.start()
          
                test_suite.runner()

                # server.stop()
            

                test_suite.pprint()

            test_suite.get_coverage()


if __name__=='__main__':
    _tini_test(*receive_args())
