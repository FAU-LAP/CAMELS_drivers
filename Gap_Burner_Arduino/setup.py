from setuptools import setup, find_packages

setup(
    name='camels_driver_gap_burner_arduino',
    version='1.0',
    description='This packes provides everything to run the LAP-custom Arduino '
                'for burning gaps into graphene with CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=['nomad_camels_support_visa_signal @ git+https://github.com/FAU-LAP/CAMELS.git@new_device_management#subdirectory=instruments/Support/visa_signal']
)