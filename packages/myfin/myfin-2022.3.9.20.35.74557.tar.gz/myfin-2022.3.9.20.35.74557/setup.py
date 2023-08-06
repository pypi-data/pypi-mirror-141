import os
from datetime import datetime
from setuptools import find_packages, setup

import git

NOW = datetime.now()

PACKAGE_NAME = 'myfin'
MAIN_PACKAGE = 'myfin'

# Get the current git hash
GIT_HASH = 'Unknown'
if os.path.exists('.git'):
    GIT_HASH = git.Repo().head.object.hexsha

# Set the package version using the build date
PACKAGE_VERSION = '{}.{}.{}.{}.{}.{}'.format(
    NOW.year, NOW.month, NOW.day, NOW.hour, NOW.minute, NOW.microsecond
)

# Set the locations of the version.py file
VERSION_PY_FILE = os.path.join(MAIN_PACKAGE, 'version.py')


# Define a function to write the version.py file
def write_version_py() -> None:
    """
    | Write the build version, so it can be accessed at runtime, via a python file.
    :return: None
    """
    content = ''.join([
        '\"\"\"', '\n',
        'THIS FILE IS GENERATED AT BUILD TIME', '\n',
        '(c) {} Markus Treppo. All rights reserved.', '\n',
        '\"\"\"', '\n', '\n',
        'version = \'{}\'', '\n',
        'git_revision = \'{}\'', '\n'
    ])
    with open(VERSION_PY_FILE, 'w') as file:
        file.write(content.format(NOW.year, PACKAGE_VERSION, GIT_HASH))


# Write the version.py file at build time
write_version_py()

# Include only the packages under the main package
PACKAGES = [MAIN_PACKAGE] + [MAIN_PACKAGE + '.' + subpackage for subpackage in find_packages(where=MAIN_PACKAGE)]

# Get the long description from README.md
LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author='Markus Treppo',
    author_email='markus.treppo@aol.com',
    packages=PACKAGES,
    description='Markus Treppo\'s personal financial risk management and visualization software.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/treppomj27/MyFin',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent'
    ],
    license='This software is the intellectual property of Markus Treppo.',
    python_requires='>=3.10'
)
