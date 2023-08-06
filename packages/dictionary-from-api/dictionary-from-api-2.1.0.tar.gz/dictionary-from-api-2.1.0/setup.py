from setuptools import setup

setup(
    name="dictionary-from-api",
    author="Osman Buğra Aydın",
    version="2.1.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
