from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='jivago',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='The Highly-Reflective Object-Oriented Python Web Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/keotl/jivago',

    author='Kento A. Lauzon',
    author_email='kento.lauzon@ligature.ca',

    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(
        exclude=['contrib', 'docs', 'tests', 'tests.*', 'example_app', 'example_app.*', 'test_data', 'test_data.*', 'test_utils', 'test_utils.*']),

    install_requires=['Jinja2', 'MarkupSafe', 'croniter', 'pyyaml', 'werkzeug'],
)
