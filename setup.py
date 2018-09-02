from os import path
from subprocess import check_output

from setuptools import setup, find_packages

git_version_command = 'git describe --tags --long --dirty'
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if path.exists(here + "/.git"):
    init_file = None
    with open(path.join(here, 'jivago/__init__.py'), 'r', encoding='utf-8') as f:
        init_file = f.read()
    if "@@VERSION@@" in init_file:
        with open(path.join(here, 'jivago/__init__.py'), 'w', encoding='utf-8') as f:
            f.write(init_file.replace("@@VERSION@@", check_output(git_version_command.split()).decode('utf-8').strip().split("-")[0]))

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
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(
        exclude=['contrib', 'docs', 'tests', 'tests.*', 'example_app', 'example_app.*', 'test_data', 'test_data.*', 'test_utils', 'test_utils.*']),

    install_requires=['Jinja2', 'MarkupSafe', 'croniter', 'pyyaml', 'werkzeug'],
)
