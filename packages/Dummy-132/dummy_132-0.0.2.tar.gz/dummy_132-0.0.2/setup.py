from versioning import updateVersion
from setuptools import setup, find_packages


def getAndUpdateVersion():
    version = updateVersion()
    return version

setup(
    name='dummy_132',
    version=getAndUpdateVersion(),
    license='MIT',
    author="uniquename21",
    author_email='uniquename21@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='dummy project'
)