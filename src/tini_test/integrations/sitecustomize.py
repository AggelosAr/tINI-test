# >>> excluded
import os
from types import FrameType
from typing import Callable


_saved = False
_store: dict[str, set] = {}

_reconcile = True


def v2_tracer(storage: dict[str, set], frame: FrameType, *args, **kwargs):
    code = frame.f_code
    file = code.co_filename
    
    file_no = frame.f_lineno

    if file not in storage:
        storage[file] = set()

    storage[file].add(file_no)
    
    return partial(v2_tracer, storage)


def register(tracer: Callable) -> None:
    sys.settrace(tracer)
    threading.settrace(tracer)

    if hasattr(threading, 'settrace_all_threads'):
        threading.settrace_all_threads(tracer)



def clear() -> None:
    sys.settrace(None)
    threading.settrace(None)

    if hasattr(threading, 'settrace_all_threads'):
        threading.settrace_all_threads(None)



if os.environ.get('TINI_TEST_COVERAGE') == '1':
    _storage_path = os.environ['TINI_TEST_COVERAGE_STORAGE']

    import atexit
    import signal
    import sys
    import threading
    from functools import partial


    if os.environ.get('USE_V2_COVERAGE'):
        # Coverage over coverage....
        tracer = partial(v2_tracer, _store)
        register(tracer)

        _reconcile = False


    from tini_test.coverage._coverage import CoverageTracker


    clear()
    tracer = partial(CoverageTracker.tracer, _store)
    register(tracer)

    
    def save_coverage() -> None:
        global _saved
        global _store
        global _storage_path

        if _saved:
            return

        
        CoverageTracker._serialize(_store=_store, 
                                   _metadata_save_path=_storage_path, 
                                   _reconcile=_reconcile)

        _saved = True


    def shutdown(*args) -> None:
        save_coverage()
        sys.exit(0)


    signal.signal(signal.SIGTERM, shutdown)
    atexit.register(save_coverage)