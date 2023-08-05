#!/usr/bin/env python

#  Copyright 2013-2014 NaviNet Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup, find_packages


DESCRIPTION = """
This library provides keywords to interact with
Openshift Cluster and perform various operations.
"""

setup(
    name='robotframework-openshift',
    version='1.0.0',
    description="Robotframework for OpenShift interactions",
    long_description=DESCRIPTION,
    author='Pablo Félix Estévez Pico',
    author_email='pestevez@redhat.com',
    url='https://github.com/red-hat-data-services/robotframework-openshift',
    license='Apache License 2.0',
    keywords='robotframework openshift',
    platforms='any',
    install_requires=[
        "reportportal-client",
        "robotframework>=4",
        "robotframework-debuglibrary",
        "robotframework-seleniumlibrary",
        "robotframework-jupyterlibrary>=0.3.1",
        "ipython",
        "openshift==0.12.1",
        "pre-commit",
        "pytest",
        "pytest-logger",
        "pyyaml",
        "pygments",
        "requests",
        "Jinja2",
        "flake8",
        "mypy",
        "kubernetes",
        "validators"
    ],
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
)
