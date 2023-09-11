# NOMAD-CAMELS Driver for Voltcraft PPS

Driver for communicating with a Voltcraft PPS power supply written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).

Implements the `VISA_Device`, `VISA_Signal_RO`, and `VISA_Signal` classes used in many device drivers.

## Features
Setting voltage and current. By giving a resistance value, one can also set a power instead of a voltage (by a given maximum current value).

## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).