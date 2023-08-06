#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests>=2',
                'requests-cache>=0.9.3',
                'jinja2>=3',
                ]

test_requirements = ['pytest>=3',
                     'jinja2>=3',
                     'requests>=2',
                     'requests-cache>=0.9.3',
                     ]

setup(
    author="Maarten Vermeyen",
    author_email='maarten@vermeyen.xyz',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=("Jinja2 extension with custom filters"
                 "replacing ORCIDs with elements from the orcid records."),
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='jinja2_orcid_extension',
    name='jinja2_orcid_extension',
    packages=find_packages(include=['jinja2_orcid_extension',
                                    'jinja2_orcid_extension.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/uantwerpen-rdm-support/jinja2_orcid_extension',
    version='0.1.0.dev1',
    zip_safe=False,
)
