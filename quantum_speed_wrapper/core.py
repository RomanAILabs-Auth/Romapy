import argparse, functools, sys, time, os, numba as nb, numpy as np

class QuantumSpeedWrapper:
    def __init__(self):
        self._compiled_funcs = {}
    def __call__(self, func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if func.__name__ not in self._compiled_funcs:
                try:
                    self._compiled_funcs[func.__name__] = nb.jit(nopython=True, fastmath=True)(func)
                except Exception:
                    return func(*args, **kwargs)
            return self._compiled_funcs[func.__name__](*args, **kwargs)
        return wrapped

def speed_wrap(): 
    return QuantumSpeedWrapper()

def cli_wrapper_main():
    parser = argparse.ArgumentParser(description="RomaPy: AI Speed Engine")
    parser.add_argument('script')
    args = parser.parse_args()
    script_path = os.path.abspath(args.script)
    sys.path.insert(0, os.path.dirname(script_path))
    with open(script_path, 'r') as f:
        env = {'__name__': '__main__', '__file__': script_path, 'speed_wrap': speed_wrap, 'np': np, 'os': os, 'sys': sys}
        exec(compile(f.read(), script_path, 'exec'), env)
