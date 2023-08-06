import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="teamleaderApiV1",
    version="0.5.0",
    url="https://github.com/HeroPP/teamleaderApiV1",
    license="MIT",
    author="Jaap",
    author_email="jaap1@me.com",
    description="Python framework on top of the teamleader v1 api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "pickle5",
        "ratelimit",
        "requests",
        "urllib3",
    ],
    packages=setuptools.find_packages(where="teamleaderApiV1"),
    python_requires=">=3.6",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
)
