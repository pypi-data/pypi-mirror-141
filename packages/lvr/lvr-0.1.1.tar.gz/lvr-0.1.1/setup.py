from setuptools import setup
from setuptools import find_packages

from glob import glob
from os.path import basename
from os.path import splitext

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='lvr',
    package_dir={'': 'lvr'},
    packages=find_packages('lvr'),
    py_modules=[splitext(basename(path))[0] for path in glob('lvr/*.py')],
    version='0.1.1',
    author='Benjamin Weber',
    author_email='mail@bwe.im',
    long_description=long_description,
    url='https://hg.sr.ht/~bwe/lvr',
    include_package_data = True,
    install_requires=[
        'numpy',
        'tabulate'
        ],
    extras_require={'test': ['pytest']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6']
    )
