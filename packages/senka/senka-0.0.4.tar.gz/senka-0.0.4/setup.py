from setuptools import setup, find_packages
from glob import glob
from os.path import splitext
from os.path import basename

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='senka',
    version='0.0.4',
    license='mit',
    description='making journal for transactions on blockchain',

    author='ca3-caaip',
    author_email='',
    url='https://github.com/ca3-caaip/senka',
    install_requires=_requires_from_file('requirements.txt'),
    extras_require={
        "test": ["pytest", "pytest-cov"]
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')]
)
