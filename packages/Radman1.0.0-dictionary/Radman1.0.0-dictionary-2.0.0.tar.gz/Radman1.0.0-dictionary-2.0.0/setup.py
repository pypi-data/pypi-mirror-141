from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="Radman1.0.0-dictionary",
    author="Radman Lotfiazar",  # TODO: Write your name
    version="2.0.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
