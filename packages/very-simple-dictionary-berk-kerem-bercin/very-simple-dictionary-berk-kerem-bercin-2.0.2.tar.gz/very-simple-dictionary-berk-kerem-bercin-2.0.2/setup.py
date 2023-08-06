from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="very-simple-dictionary-berk-kerem-bercin",
    author="Berk Kerem Berçin",  # TODO: Write your name
    version="2.0.2",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
