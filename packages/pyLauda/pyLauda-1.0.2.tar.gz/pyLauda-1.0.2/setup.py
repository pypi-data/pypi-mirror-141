# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path
import io

here = path.abspath(path.dirname(__file__))

# get the log description
with io.open(path.join(here, "DESCRIPTION.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup_requires = ['pyserial']


setup(
    name='pyLauda',
    version='1.0.2',
    description='German Aerospace Center',
    long_description=long_description,
    url='https://gitlab.com/Egenskaber/pylauda',
    author='German Aerospace Center',
    author_email="konstantin+pypi@niehaus-web.com",
    install_requires=setup_requires,
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='driver, rs232, rs485, temperature control, lauda',
    packages=['pyLauda'],
    package_data={ "pyLauda" : ['']},

)
