import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="boticordpy",
    version="1.2.1",
    description="Simple Python Module for boticord api",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/grey-cat-1908/boticordpy",
    author="KerdokuCat",
    author_email="support@kerdoku.top",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["discord.py", "aiohttp", "asyncio"],
)
