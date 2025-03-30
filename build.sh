#!/bin/bash
# Build script for Sabbath School Lessons package

# Install requirements for version checker
pip install requests packaging

# Run version checker to auto-increment version if needed
pythonPath=$(which python 2>/dev/null)
if [ -z "$pythonPath" ]; then
    pythonPath=$(which python3 2>/dev/null)
fi

if [ -z "$pythonPath" ]; then
    echo "Error: Python not found in PATH"
    exit 1
fi

echo "Using Python at: $pythonPath"

# Run version checker
package_name=$($pythonPath versionChecker.py)
if [ -z "$package_name" ]; then
    echo "Error: Failed to get package name from versionChecker.py"
    exit 1
fi

echo "Package name: $package_name"

# Ensure we have the latest build tools
pip install --upgrade pip setuptools wheel build

# Clean previous builds
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/

# Build the package
echo "Building package..."
$pythonPath -m build

# Show output
echo "Build complete. Distribution files created in dist/ directory."
echo "To install globally, run: pip install dist/*.whl"
echo "To upload to PyPI, run: twine upload dist/*"