from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="q1q1-dictionary",
    author="Barış Tiftik",
    version="2.0.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
