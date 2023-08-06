import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

build_major = 0
build_minor = os.getenv('GITHUB_RUN_NUMBER')
if build_minor is None:
    raise Exception('GITHUB_RUN_NUMBER is not set')
build_number = f"{build_major}.{build_minor}"

setup(
    name='django-simple-worker',
    version=build_number,
    description='Django Simple Worker',
    url='https://www.idea-loop.com/',
    author='idealoop',
    author_email='noreply@idea-loop.com',
    license='MIT',
    packages=find_packages(exclude=["tests.*", "tests", "test*"]),
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'django',
    ],
    zip_safe=False
)
