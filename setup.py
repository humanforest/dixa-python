#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ["pydantic", "pandas", "requests", "phonenumbers", "pydantic[email]"]

test_requirements = ['pytest>=3']

setup(
    author="José Duarte",
    author_email='jose.duarte@humanforest.co.uk',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description="Dixa Developer Kit for Python",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='dixa',
    name='dixa',
    packages=find_packages(include=['dixa', 'dixa.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/humanforest/dixa-python',
    version='0.1.0',
    zip_safe=False,
)
