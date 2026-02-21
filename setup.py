from setuptools import setup, find_packages

setup(
    name='quantum_speed_wrapper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numba', 'numpy', 'joblib', 'psutil', 'tqdm', 'python-dotenv', 'prometheus-client'
    ],
    entry_points={
        'console_scripts': [
            'romapy = quantum_speed_wrapper.core:cli_wrapper_main',
        ],
    },
)
