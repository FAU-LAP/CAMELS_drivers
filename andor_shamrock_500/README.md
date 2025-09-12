# NOMAD-CAMELS Driver for Andor Shamrock 500

This package provides a driver of the Andor Shamrock 500 spectrometer for the measurement software [NOMAD CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).\
It uses [pylablib](https://pylablib.readthedocs.io/en/latest/devices/AndorShamrock.html) for communication.

<div style="border: 1px solid black; padding: 10px; background-color: #b3d8adff; color: black;">
  <strong>Note:</strong> You may need additional software requirements, like the vendor's <code style="color: black">dll</code> files. See the <a href="https://pylablib.readthedocs.io/en/latest/devices/AndorShamrock.html">pylablib documentation</a> for that.
</div>


## Features
Needs to connect with an Andor camera. Note that the camera has to be an instrument in CAMELS as well.

Apart from reading the spectra, the driver supports setting the wavelengths, input / output slit size and the grating.

Additionally a manual control for taking single spectra and controlling the settings is included. Note that a protocol by default still uses the settings from the "Manage Instruments" dialog in CAMELS!

## Documentation

For more information and documentation visit the [CAMELS documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).


## Changelog

### 0.1.4
Improved metadata

### 0.1.3
Small bugfix for UI on first start

### 0.1.2
Fixed closing the manual control on error so it can be restarted without restarting CAMELS.