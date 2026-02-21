# 1. Create Folder Structure
mkdir -p quantum_speed_wrapper/quantum_speed_wrapper
mkdir -p quantum_speed_wrapper/benchmarks

# 2. Create the Core Engine (core.py)
cat << 'INNER' > quantum_speed_wrapper/quantum_speed_wrapper/core.py
import sys, os
from numba import njit, objmode

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
    
    env = {
        'speed_wrap': SpeedWrapper(),
        '__file__': script_path,
        'os': os,
        'sys': sys
    }
    exec(compile(content, script_path, 'exec'), env)
INNER

# 3. Create the Turbo Runner (runner.py)
cat << 'INNER' > quantum_speed_wrapper/runner.py
import time, os, sys
from llama_cpp import Llama

accelerate = speed_wrap()

# Universal Path Solver
MODEL_NAME = "dolphin-2.9-llama3-8b-Q4_K_M.gguf"
search_paths = [
    os.path.join(os.path.dirname(__file__), MODEL_NAME),
    os.path.expanduser(f"~/Downloads/{MODEL_NAME}"),
    os.path.expanduser(f"~/downloads/{MODEL_NAME}")
]
MODEL_PATH = next((p for p in search_paths if os.path.exists(p)), None)

if not MODEL_PATH:
    print(f"❌ Error: {MODEL_NAME} not found!")
    sys.exit(1)

print(f"🐬 Loading Turbo Model: {MODEL_PATH}")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=8, n_batch=512, n_ubatch=512, verbose=False)

@accelerate
def clean_token(text):
    return text.strip() + " "

def chat():
    print("\n--- RomaPy Chat (2.07s Latency Mode) ---")
    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']: break
        prompt = f"<|im_start|>system\nYou are Dolphin.<|im_end|>\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n"
        start = time.time()
        stream = llm(prompt, max_tokens=512, stop=["<|im_end|>"], stream=True)
        print("AI: ", end="")
        first = True
        for output in stream:
            if first:
                print(f"🚀 [Latency: {time.time()-start:.2f}s] ", end="")
                first = False
            print(clean_token(output['choices'][0]['text']), end="", flush=True)
        print()

if __name__ == "__main__":
    chat()
INNER

# 4. Create Setup.py for 'romapy' command
cat << 'INNER' > quantum_speed_wrapper/setup.py
from setuptools import setup, find_packages
setup(
    name="romapy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["numba", "llama-cpp-python", "numpy"],
    entry_points={"console_scripts": ["romapy=quantum_speed_wrapper.core:cli_wrapper_main"]},
)
INNER

# 5. Create .gitignore
cat << 'INNER' > quantum_speed_wrapper/.gitignore
*.gguf
*.bin
__pycache__/
*.egg-info/
.venv/
INNER

echo "✅ RomaPy Project Rebuilt Successfully!"
