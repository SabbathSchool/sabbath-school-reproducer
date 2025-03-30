#!/bin/bash
# Script to upload the Sabbath School Lessons package to PyPI

# Check if twine is installed, install if not
pip install -q twine

# Upload to PyPI
echo "Uploading package to PyPI..."
python -m twine upload dist/* --verbose

echo "Upload complete."