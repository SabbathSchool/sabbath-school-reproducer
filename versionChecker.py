import requests
import re
import os
import sys
from packaging import version

def find_package_name():
    """Find the package name from setup.py"""
    try:
        with open(os.path.join("setup.py"), "r") as f:
            setup_content = f.read()
            match = re.search(r"name\s*=\s*[\"']([^\"']*)[\"']", setup_content)
            if match:
                return match.group(1)
            
        # Fallback to looking in src directory
        with open(os.path.join("src", "sabbath_school_lessons", "__init__.py"), "r") as f:
            init_content = f.read()
            version_match = re.search(r"__version__\s*=\s*[\"']([^\"']*)[\"']", init_content)
            if version_match:
                return "sabbath-school-reproducer"
    except FileNotFoundError:
        pass
    
    return "sabbath-school-reproducer"  # Default fallback

def check_package_version():
    """Check the latest version of the package on PyPI"""
    package_name = find_package_name()
    
    # URL of the package on PyPI
    package_url = f"https://pypi.org/pypi/{package_name}/json"
    
    # Get the JSON response
    try:
        response = requests.get(package_url)
        if response.status_code == 200:
            # Parse JSON response
            package_info = response.json()
            
            # Extract the latest version from the parsed JSON
            latest_version = package_info["info"]["version"]
            return latest_version
        elif response.status_code == 404:
            return "0.0.0"  # Package not found on PyPI
        else:
            return False
    except requests.RequestException:
        return False

def get_local_version():
    """Get the local version from setup.py or __init__.py"""
    try:
        # Try to get version from setup.py
        with open("setup.py", "r") as f:
            setup_content = f.read()
        
        local_version_match = re.search(r"version=['\"]([^'\"]*)['\"]", setup_content)
        if local_version_match:
            return local_version_match.group(1)
        
        # Fallback to __init__.py
        with open(os.path.join("src", "sabbath_school_lessons", "__init__.py"), "r") as f:
            init_content = f.read()
        
        init_version_match = re.search(r"__version__\s*=\s*[\"']([^\"']*)[\"']", init_content)
        if init_version_match:
            return init_version_match.group(1)
    except FileNotFoundError:
        pass
    
    return "0.1.0"  # Default fallback

def local_version_needs_update(local_version, latest_version):
    """Check if local version needs an update"""
    return version.parse(local_version) <= version.parse(latest_version)

def update_local_version(local_version, latest_version):
    """Generate an updated version number"""
    if local_version_needs_update(local_version, latest_version):
        parts = latest_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)  # Increment the patch number
        new_version = '.'.join(parts)
        return new_version
    else:
        return local_version

def update_version_in_files(new_version):
    """Update version in setup.py and __init__.py"""
    files_updated = False
    
    # Update setup.py
    try:
        with open("setup.py", "r") as f:
            setup_content = f.read()
        
        updated_content = re.sub(
            r"version=['\"][^'\"]*['\"]", 
            f"version=\"{new_version}\"", 
            setup_content
        )
        
        with open("setup.py", "w") as f:
            f.write(updated_content)
        
        files_updated = True
    except FileNotFoundError:
        pass
    
    # Update __init__.py
    try:
        init_path = os.path.join("src", "sabbath_school_lessons", "__init__.py")
        with open(init_path, "r") as f:
            init_content = f.read()
        
        updated_content = re.sub(
            r"__version__\s*=\s*[\"'][^\"']*[\"']", 
            f"__version__ = \"{new_version}\"", 
            init_content
        )
        
        with open(init_path, "w") as f:
            f.write(updated_content)
        
        files_updated = True
    except FileNotFoundError:
        pass
    
    return files_updated

def main():
    """Main function to check and update version"""
    package_name = find_package_name()
    latest_version = check_package_version()
    
    if not latest_version:
        latest_version = "0.0.0"
    
    local_version = get_local_version()
    
    if local_version_needs_update(local_version, latest_version):
        new_version = update_local_version(local_version, latest_version)
        update_version_in_files(new_version)
        print(f"Updated version from {local_version} to {new_version}")
    else:
        print(f"Current version {local_version} is up to date")
    
    print(package_name)
    return package_name

if __name__ == "__main__":
    # Get the function name from command line argument, defaulting to "main"
    function_name = sys.argv[1] if len(sys.argv) > 1 else "main"
    
    # Call the specified function
    if function_name == "main":
        main()