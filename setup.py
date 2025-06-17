from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="docext",
    version="0.1.13",
    author="Souvik Mandal",
    author_email="souvik@nanonets.com",
    description="Onprem information extraction from documents",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nanonets/docext",
    packages=find_packages(include=["docext", "docext.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    dependency_links=[
        "https://github.com/huggingface/transformers/tarball/49b5ab6a27511de5168c72e83318164f1b4adc43#egg=transformers",
    ],
    extras_require={
        "dev": ["pre-commit"],
    },
    entry_points={
        "console_scripts": [
            "docext=docext.__main__:main",
        ],
    },
    include_package_data=True,
)
