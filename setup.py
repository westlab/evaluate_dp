from setuptools import setup

install_requires = [
    "numpy",
    "pandas",
    "matplotlib",
    "PyYAML",
]

packages = ["dp"]

setup(
    name="evaluate_dp",
    version="0.0.0",
    author="WestLab",
    packages=packages,
    install_requires=install_requires,
)
