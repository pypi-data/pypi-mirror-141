from setuptools import setup

setup(
    name="berks-very-simple-dictionary",
    author="Berk Takıt",
    version="2.0.2",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
