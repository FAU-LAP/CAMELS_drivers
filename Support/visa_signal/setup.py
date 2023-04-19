from setuptools import setup, find_packages

setup(
    name='camels_support_visa_signal',
    version='1.0',
    description='This package is used to implement simple communication with'
                'VISA devices using bluesky',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=['ophyd>=1.6.4',
                      'PyVISA>=1.12.0',
                      'PyVISA-py>=0.5.3']
)