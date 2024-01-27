#!/usr/bin/env python3
import os
import re
import subprocess


def update_version():
    version_pattern = re.compile(r'version="(\d+\.\d+\.\d+)"')
    with open('setup.py', 'r') as file:
        content = file.read()
    current_version = version_pattern.search(content).group(1)
    major, minor, patch = map(int, current_version.split('.'))
    new_version = f'{major}.{minor}.{patch + 1}'
    updated_content = version_pattern.sub(f'version="{new_version}"', content)
    with open('setup.py', 'w') as file:
        file.write(updated_content)
    return new_version

def build_package():
    subprocess.check_call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])

def publish_package():
    subprocess.check_call(['twine', 'upload', 'dist/*'], env={
        'TWINE_USERNAME': os.environ.get('TWINE_USERNAME'),
        'TWINE_PASSWORD': os.environ.get('TWINE_PASSWORD')
    })

def main():
    update_version()
    build_package()
    publish_package()

if __name__ == '__main__':
    main()
