# NOMAD Camels driver for adc_x418

Driver for X-418 analog data acquisition system written for the measurement software [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/).

## Features

The driver supports readout from 8 channels (only tested for single-ended voltage input), setting ranges for each channel separately, setting resolution for all channels simultaneously. The driver has been tested with Ubuntu 24.04.1 LTS with X-418 connected via ethernet switch to the PC (local network with fixed IP addresses).

## Important details

X-418 must be set up according to the user manual before connecting to it via CAMELS. Check that X-418 can be accessed via browser (http://<ip-address>/setup.html#) before running the driver.

If you only plan to read the values from X-418 and do not need to change range or resolution, "user" account of X-418 is sufficient and password does not have to be entered every time the protocol utilising X-418 is run. In this case uncheck "Use admin credentials (necessary for changing settings of X418)" field in "Configure Instruments". All changes to range and resolution will be ignored, including the values in "Configure Instruments" dialog, and X-418 will continue using the previously set parameters.

If you plan to set or change range and resolution via CAMELS, "admin" account must be used.

If you have X-418 connected over public network, it is highly recommended to set up "user" password. Please refer to the user manual for instructions. 

Range for every channel can be entered as arbitrary number in a range of [0, 10.24] V. As device support only fixed set of possible ranges, the value entered will be rounded up to the next possible range.

Resolution setting applies to all channels simultaneously. It defines number of decimal digits after "." shown for measured values.

For security reasons, the device password is not saved in .nxs file, unlike all other metadata.

## Documentation

For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).