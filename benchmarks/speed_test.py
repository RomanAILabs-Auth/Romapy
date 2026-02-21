import numpy as np
import time

accelerate = speed_wrap()

@accelerate
def heavy_math(data):
    result = np.zeros_like(data)
    for i in range(len(data)):
        result[i] = np.sqrt(data[i] ** 2 + 100) / 2
    return result

data = np.random.rand(10_000_000)
print(f"Testing 10 Million operations...")
start = time.time()
heavy_math(data)
print(f"✅ RomaPy Execution Time: {time.time() - start:.4f} seconds")
