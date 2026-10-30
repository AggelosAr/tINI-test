import os

_saved = False


if os.environ.get('TINI_TEST_COVERAGE') == '1':
    import signal
    import sys
    import threading
    import atexit
    from functools import partial
    from tini_test.coverage._coverage import CoverageTracker


    def save_coverage() -> None:
        global _saved

        if _saved:
            return
        
        _saved = True

        storage_path = os.environ['TINI_TEST_COVERAGE_STORAGE']
        tracker = CoverageTracker(runtime_covered_lines=storage,
                                  metadata_save_path=storage_path)
        tracker.serialize()


    def shutdown() -> None:
        save_coverage()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    

    storage = {}
    tracer = partial(CoverageTracker.tracer, storage)

    sys.settrace(tracer)
    threading.settrace(tracer)


    # TODO does the default context manager needs this as well?
    if hasattr(threading, 'settrace_all_threads'):
        threading.settrace_all_threads(tracer)


    atexit.register(save_coverage)
    