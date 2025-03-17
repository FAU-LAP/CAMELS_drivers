# NOMAD Camels driver for iBeam_smart

Driver for iBeam_smart written for the measurement software [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/).
This driver utilizes the iBeam smart driver from [pylablib](https://pylablib.readthedocs.io/en/latest/devices/Toptica.html) in the backend and simply offers a front end for CAMELS. It dynamically creates all set and read channels for each channel of the laser.

This driver is licensed under GPL 3 due to using the pylablib backend.

## Changes

- Fixed imports and class names: You can now combine multiple types of dynamically created instruments (like EPICS, OPC-UA instruments and iBeam smart) in a single measurement.

## Documentation

For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).