from os import path
from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='the-magic-lib',
    packages=find_packages(include=['magic_lib']),
    version='0.1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://magic-lib.readthedocs.io/",
    description='The magic library',
    author='Louis Nourigeon',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)