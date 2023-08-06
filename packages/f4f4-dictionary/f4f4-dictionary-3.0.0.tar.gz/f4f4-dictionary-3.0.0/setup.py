from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="f4f4-dictionary",
    author="Barış Tiftik",
    version="3.0.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
