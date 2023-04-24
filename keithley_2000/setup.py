from setuptools import setup, find_packages

setup(
    name='camels_driver_keithley_2000',
    version='1.0',
    description='This packes provides everything to run the Keithley 2000 '
                'digital multimeter with CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=['camels_support_visa_signal @ git+https://github.com/FAU-LAP/CAMELS.git@new_device_management#subdirectory=instruments/Support/visa_signal']
)