from setuptools import setup, find_packages


setup(
    name="fantasyfootball",
    version="0.1.0",
    packages=find_packages(exclude=("tests*", "testing*"),),
)
