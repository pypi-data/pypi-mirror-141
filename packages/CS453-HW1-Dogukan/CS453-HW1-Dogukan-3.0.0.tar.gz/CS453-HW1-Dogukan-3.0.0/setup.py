from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="CS453-HW1-Dogukan",
    author="Doğukan Ertunga Kurnaz",  # TODO: Write your name
    version="3.0.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
#For trigger initial ci/cd run. todo: remove this line.