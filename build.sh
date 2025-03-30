#!/bin/bash
# Build script for Sabbath School Lessons package

# Ensure we have the latest build tools
pip install --upgrade pip setuptools wheel build

# Clean previous builds
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/

# Build the package
python -m build

echo "Build complete. Distribution files created in dist/ directory."
echo "To install globally, run: pip install dist/*.whl"
echo "To upload to PyPI, run: twine upload dist/*"ch