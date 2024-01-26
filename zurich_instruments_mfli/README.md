# NOMAD-CAMELS Driver for Zurich Instruments lock-in amplifier MFLI

This is a basic driver designed to be able to control the Zurich Instruments
lock-in amplifier MFLI in NOMAD-CAMELS. Its implementation relies on `zhinst`.
This integration does not fully cover the device's capabilities, but it can be
used as a base to develop a more feature-rich driver for this device.

Some of the functionality accessible over the web interface is implemented.

Other functionality, that concerns setting values can also be accessed via the
`set_double` and `set_int` functions: call the channel `set_double` or `set_int`
and pass a string of the path to the functionality of the lock-in (without the
device name) with a ':' and then the value you want to set. The string should
conform with this format: 'PATH/TO/FUNCTIONALITY:VALUE'. Do not forget the
inverted commas in CAMELS, otherwise it will be interpreted as python code.

Many parameters that can be set, but do not need to be set via a variable, such
as the number of the harmonic you want to measure, are included in the
configuration to give a better overview.


## Useful Links

- [NOMAD-CAMELS Documentation](https://fau-lap.github.io/NOMAD-CAMELS/index.html)
- [NOMAD-CAMELS: create new instrument drivers documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/programmers_guide/instrument_drivers.html)
- [Zurich Instruments lock-in amplifier MFLI manual](https://docs.zhinst.com/pdf/ziMFLI_UserManual.pdf)
