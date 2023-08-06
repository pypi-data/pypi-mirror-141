from distutils.core import setup

version_number = '0.1.1'
setup(
    name='qvalue',
    version=version_number,
    description=
    'Converts p-values in q-values in order to account for multiple hypotheses testing, see (Storey and Tibshirani, 2003)',
    long_description=open('README.md').read(),
    author='byoryn',
    author_email='barwechin@163.com',
    packages=['qvalue'],
    requires=['numpy (>=1.5)', 'scipy (>=0.8)'],
    license='3-clause BSD',
)
