#!/usr/bin/env python3
"""
Setup Script for Sabbath School Lesson Downloader

This script helps with setting up the required dependencies.
"""

from setuptools import setup, find_packages

setup(
    name="sabbath-school-lessons",
    version="0.1.0",
    description="Download and process Sabbath School lessons from GitHub",
    author="Gospel Sounders",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.1",
        "requests>=2.22.0",
        "markdown>=3.1.1",
        "weasyprint>=51.0",
        "beautifulsoup4>=4.8.0",
    ],
    entry_points={
        "console_scripts": [
            "sabbath-school-downloader=main:main",
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