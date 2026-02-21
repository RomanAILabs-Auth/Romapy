from setuptools import setup, find_packages
setup(
    name="romapy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["numba", "llama-cpp-python", "numpy"],
    entry_points={"console_scripts": ["romapy=quantum_speed_wrapper.core:cli_wrapper_main"]},
)
