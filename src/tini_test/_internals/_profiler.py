

def profiler(is_profiling: bool = False):

    def wraper(func):

        def _wrapped(*args, **kwargs):

            if is_profiling:
                from pyinstrument import Profiler
                profiler = Profiler()
                profiler.start()
                
            result = func(*args, **kwargs)

            if is_profiling:
                profiler.stop()
                with open("profile.html", "w") as f:
                    f.write(profiler.output_html())

            return result

        return _wrapped

    return wraper
