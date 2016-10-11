# All code provided from the http://gengo.com site, such as API example code
# and libraries, is provided under the New BSD license unless otherwise
# noted. Details are below.
#
# New BSD License
# Copyright (c) 2009-2015, Gengo, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# Neither the name of Gengo, Inc. nor the names of its contributors may
# be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Original Author: Ryan McGrath <http://venodesigns.net>

import sys
import os
from distutils.core import Command
from setuptools import setup
from setuptools import find_packages
from subprocess import call

# little tricky, but this is for version number is in one place.
__version__ = 'This value will be overridden by exec.'
exec(open('gengo/_version.py').read())

# Command based on Libcloud setup.py:
# https://github.com/apache/libcloud/blob/trunk/setup.py


class Pep8Command(Command):
    description = "Run pep8 script"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pep8
            pep8
        except ImportError:
            print ('Missing "pep8" library. You can install it using pip: '
                   'pip install pep8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = call(('pep8 {0}/gengo/'.format(cwd)).split(' '))
        sys.exit(retcode)


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'gengo/tests.py'])
        raise SystemExit(errno)

setup(
    # Basic package information.
    name='gengo',
    version=__version__,
    packages=find_packages(),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=["requests >= 2.2.1"],

    # Metadata for PyPI.
    author='Gengo',
    author_email='api@gengo.com',
    license='New BSD License',
    url='https://github.com/gengo/gengo-python',
    keywords='gengo translation language api',
    description='Official Python library for interfacing with the Gengo API.',
    long_description=open('README.md').read(),
    cmdclass={
        'pep8': Pep8Command,
        'test': TestCommand,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
