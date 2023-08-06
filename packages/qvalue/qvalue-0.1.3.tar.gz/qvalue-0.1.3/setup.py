from distutils.core import setup

version_number = '0.1.3'
setup(
    name='qvalue',
    version=version_number,
    description='',
    author='byoryn',
    author_email='barwechin@163.com',
    packages=['qvalue'],
    requires=['numpy (>=1.5)', 'scipy (>=0.8)'],
    license='3-clause BSD',
)
