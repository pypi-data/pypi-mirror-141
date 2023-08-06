from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="aaaa-dictionary",
    author="Barış Tiftik",
    version="3.0.1",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
