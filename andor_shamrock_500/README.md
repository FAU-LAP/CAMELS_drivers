# NOMAD-CAMELS Driver for Andor Shamrock 500

This package provides a driver of the Andor Shamrock 500 spectrometer for the measurement software [NOMAD CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).\
It uses [pylablib](https://pylablib.readthedocs.io/en/latest/devices/AndorShamrock.html) for communication.


## Documentation

For more information and documentation visit the [CAMELS documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).


## Changelog

### 0.1.2
Fixed closing the manual control on error so it can be restarted without restarting CAMELS.