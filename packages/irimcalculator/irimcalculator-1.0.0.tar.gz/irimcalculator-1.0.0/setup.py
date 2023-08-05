from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="irimcalculator",
    version="1.0.0",
    description="Calculator with bacis operations",
    license="MIT",
    long_description=long_description,
    author="Indre Rimkeviciene",
    author_email="i.kirsanskaite@gmail.com",
    packages=["calculator_project"],
)
