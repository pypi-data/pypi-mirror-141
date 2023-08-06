from glob import glob
from os.path import basename
from os.path import splitext
import os

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

version = os.environ.get("package_version", "0.0.1")

setup(
    name="spark-wheel-test",
    version=version,
    author="Daniel Yu",
    author_email="daniel.yu@ipt.ch",
    description="A small example package to demonstrate how to build helper classes using pyspark.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'  # Best to match this with the Databricks Runtime you are targeting
)