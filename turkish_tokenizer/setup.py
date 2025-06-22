#!/usr/bin/env python3
"""
Setup script for Turkish Tokenizer package.
"""

import os

from setuptools import find_packages, setup


# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read version from version.py
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "version.py")
    with open(version_file, "r", encoding="utf-8") as f:
        exec(f.read())
    return locals()["__version__"]

setup(
    name="turkish-tokenizer",
    version=get_version(),
    author="Ali Bayram",
    author_email="malibayram20@gmail.com",
    description="High-performance morphological tokenizer for Turkish text with Rust backend",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/turkish-tokenizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "turkish-tokenizer=turkish_tokenizer.cli:main",
        ],
    },
    package_data={
        "turkish_tokenizer": ["*.json"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="turkish tokenizer nlp morphological bpe rust",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/turkish-tokenizer/issues",
        "Source": "https://github.com/yourusername/turkish-tokenizer",
        "Documentation": "https://github.com/yourusername/turkish-tokenizer#readme",
    },
) 