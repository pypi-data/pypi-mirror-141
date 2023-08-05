from setuptools import setup

install_requirements = [
    "tensorboard",
    "torch-tb-profiler",
    "geneticalgorithm2",
    "TA-Lib",
    "ritl",
    "pandas-ta"
]

setup(
    install_requires=install_requirements,
)
