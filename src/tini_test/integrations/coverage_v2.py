from functools import partial
import os


if os.environ.get('USE_V2_COVERAGE'):
    def tracer(storage, frame, *args, **kwargs):
        code = frame.f_code
        file = code.co_filename
        
        file_no = frame.f_lineno
    
        if file not in storage:
            storage[file] = set()
        storage[file].add(file_no)
        
        return partial(tracer, storage)
    