# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wifi_connect",
    version="0.0.2",
    author="Xairi Valdivia",
    author_email="xairi.valdivia@gmail.com",
    description="List and connect to wifi networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Prometeo136/wifi-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    scripts=["bin/wifi-connect"],
)
