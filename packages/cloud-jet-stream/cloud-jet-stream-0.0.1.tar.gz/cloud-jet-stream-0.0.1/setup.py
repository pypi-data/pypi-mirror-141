# https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html

from setuptools import setup, find_packages

setup(
    name='cloud-jet-stream',
    version='0.0.001',
    author='Ryan Moos',
    author_email='ryan@moos.engineering',
    packages=find_packages(),
    scripts=['bin/jet-stream'],
    url='http://pypi.python.org/pypi/jet-stream/',
    license='LICENSE',
    description='AWS Cloud Development Toolkit',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "aws-cdk-lib",
        "boto3",
        "pyopenssl"
    ],
)

