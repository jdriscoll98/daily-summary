#!/usr/bin/env python3
import os
import re
import subprocess
import sys


def update_version_in_setup(new_version):
    setup_file_path = 'setup.py'
    with open(setup_file_path, 'r') as file:
        content = file.read()
    content = re.sub(r'version="[0-9]+\.[0-9]+\.[0-9]+"', f'version="{new_version}"', content)
    with open(setup_file_path, 'w') as file:
        file.write(content)

def build_package():
    subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], check=True)

def upload_to_pypi():
    result = subprocess.run(['twine', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Twine is not installed. Please install it with 'pip install twine'.")
        sys.exit(1)
    subprocess.run(['twine', 'upload', 'dist/*'], check=True)

def is_valid_version(version):
    return re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', version) is not None

def main():
    if len(sys.argv) != 2:
        print("Usage: publish.py <new_version>")
        sys.exit(1)
    new_version = sys.argv[1]
    if not is_valid_version(new_version):
        print("Error: Invalid version format. Please use MAJOR.MINOR.PATCH.")
        sys.exit(1)
    update_version_in_setup(new_version)
    build_package()
    upload_to_pypi()

if __name__ == "__main__":
    main()
    os.chmod('scripts/publish.py', 0o755)
