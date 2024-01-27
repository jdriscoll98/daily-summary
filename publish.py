#!/usr/bin/env python3
import os
import re
import subprocess


def update_version():
    setup_path = 'setup.py'
    version_pattern = re.compile(r"(version=['\"])([\d.]+)(['\"])")
    with open(setup_path, 'r') as file:
        content = file.read()
    current_version = version_pattern.search(content).group(2)
    version_parts = current_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    updated_content = version_pattern.sub(r'\g<1>{}\g<3>'.format(new_version), content)
    with open(setup_path, 'w') as file:
        file.write(updated_content)
    return new_version

def build_package():
    result = subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], check=True)
    if result.returncode != 0:
        raise Exception('Building the package failed.')

def publish_package():
    result = subprocess.run(['twine', 'upload', 'dist/*'], check=True)
    if result.returncode != 0:
        raise Exception('Publishing the package failed.')

if __name__ == '__main__':
    try:
        new_version = update_version()
        print(f'Updated package version to {new_version}')
        build_package()
        print('Package build successful.')
        publish_package()
        print('Package published successfully.')
    except Exception as e:
        print(str(e))
        exit(1)
