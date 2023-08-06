import pathlib
import setuptools
from pathlib import Path

setuptools.setup(
    name="xuleipdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # 将不需要的包排除在外
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
