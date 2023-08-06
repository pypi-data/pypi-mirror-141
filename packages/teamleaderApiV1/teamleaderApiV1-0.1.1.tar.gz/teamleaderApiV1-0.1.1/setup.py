from setuptools import setup

setup(
    name="teamleaderApiV1",
    packages=["teamleaderApiV1"],
    version="0.1.1",
    url="https://github.com/HeroPP/teamleaderApiV1",
    license="MIT",
    author="Jaap",
    author_email="jaap1@me.com",
    description="Python framework on top of the teamleader v1 api",
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "pickle5",
        "ratelimit",
        "requests",
        "urllib3",
    ],
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
