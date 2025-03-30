#!/usr/bin/env python3
"""
Setup Script for Sabbath School Lesson Downloader

This script packages the application for distribution.
"""

from setuptools import setup, find_packages
import os

# Read requirements from file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Create data files list to include non-Python files
data_files = [
    ('bin', ['src/sabbath_school_reproducer/bin/run.sh', 
             'src/sabbath_school_reproducer/bin/generate_config.py']),
]

setup(
    name="sabbath-school-reproducer",
    version="0.1.0",
    description="Download and process Sabbath School lessons from GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gospel Sounders",
    author_email="youremail@example.com",
    url="https://github.com/SabbathSchool/sabbath-school-reproducer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    data_files=data_files,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sabbath-school-downloader=sabbath_school_reproducer.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)