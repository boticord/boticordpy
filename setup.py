import pathlib

from setuptools import setup, find_packages
import re

HERE = pathlib.Path(__file__).parent

with open("boticordpy/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if version.endswith(("a", "b", "rc")):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass

README = (HERE / "README.md").read_text(encoding="utf8")

setup(
    name="boticordpy",
    project_urls={
        "Documentation": "https://py.boticord.top/en/stable",
        "Issue tracker": "https://github.com/boticord/boticordpy/issues",
    },
    packages=find_packages(),
    version=version,
    python_requires=">= 3.6",
    description="A Python wrapper for BotiCord API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/boticord/boticordpy",
    author="Marakarka",
    author_email="support@kerdoku.top",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["aiohttp"],
)
