import os

_saved = False
_store = {}


if os.environ.get('TINI_TEST_COVERAGE') == '1':
    _storage_path = os.environ['TINI_TEST_COVERAGE_STORAGE']

    import signal
    import sys
    import threading
    import atexit
    from functools import partial

    if os.environ.get('USE_V2_COVERAGE'):
        # Coverage over coverage....
        from tini_test.integrations.coverage_v2 import tracer
        tracer = partial(tracer, _store)
    else:
        from tini_test.coverage._coverage import CoverageTracker
        tracer = partial(CoverageTracker.tracer, _store)

    
    def save_coverage() -> None:
        global _saved
        global _store
        global _storage_path

        if _saved:
            return

        from tini_test.coverage._coverage import CoverageTracker
        CoverageTracker._serialize(_store=_store, _metadata_save_path=_storage_path)

        _saved = True


    def shutdown() -> None:
        save_coverage()
        sys.exit(0)


    signal.signal(signal.SIGTERM, shutdown)
    atexit.register(save_coverage) 


    sys.settrace(tracer)
    threading.settrace(tracer)

    # TODO does the default context manager needs this as well?
    # XXX general insight: can we have multiple tracers active at the same time?
    if hasattr(threading, 'settrace_all_threads'):
        threading.settrace_all_threads(tracer)
