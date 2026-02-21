import sys, os
from numba import njit

class SpeedWrapper:
    def __init__(self):
        self._compiled_funcs = {}
    def __call__(self, func):
        def wrapped(*args, **kwargs):
            if func.__name__ not in self._compiled_funcs:
                self._compiled_funcs[func.__name__] = njit(func)
            return self._compiled_funcs[func.__name__](*args, **kwargs)
        return wrapped

def cli_wrapper_main():
    if len(sys.argv) < 2:
        print("Usage: romapy <script.py>")
        return
    script_path = os.path.abspath(sys.argv[1])
    with open(script_path, 'r') as f:
        content = f.read()
    env = {'speed_wrap': SpeedWrapper(), '__file__': script_path, 'os': os, 'sys': sys}
    exec(compile(content, script_path, 'exec'), env)
