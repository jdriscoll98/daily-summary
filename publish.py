#!/usr/bin/env python3
import os
import re
import subprocess


def read_current_version():
    with open('setup.py', 'r') as file:
        content = file.read()
        version_match = re.search(r"version=['\"](.*?)['\"]", content)
        if version_match:
            return version_match.group(1)
        raise RuntimeError('Could not find the version in setup.py')

def increment_version(current_version):
    major, minor, patch = map(int, current_version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

def write_new_version(new_version):
    with open('setup.py', 'r') as file:
        content = file.read()
    content = re.sub(r"(version=['\"])(.*?)(['\"])", r'\g<1>' + new_version + r'\3', content)
    with open('setup.py', 'w') as file:
        file.write(content)

def build_package():
    result = subprocess.run(['python3', 'setup.py', 'sdist', 'bdist_wheel'], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Building package failed: {result.stderr}")

def publish_package():
    username = os.environ.get('PYPI_USERNAME', '__token__')
    password = os.environ.get('PYPI_TOKEN')
    if not password:
        raise RuntimeError('PYPI_TOKEN environment variable is not set')
    result = subprocess.run(['twine', 'upload', 'dist/*', '-u', username, '-p', password], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Publishing package failed: {result.stderr}")

if __name__ == "__main__":
    current_version = read_current_version()
    new_version = increment_version(current_version)
    write_new_version(new_version)
    build_package()
    publish_package()
