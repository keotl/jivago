from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='jivago',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='A Python framework for writing Java-esque REST applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/keotl/jivago',

    author='Kento A. Lauzon',
    author_email='kento.lauzon@ligature.ca',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(
        exclude=['contrib', 'docs', 'tests', 'tests.*', 'example_app', 'example_app.*', 'test_data', 'test_data.*']),

    install_requires=['Jinja2', 'MarkupSafe'],
)
