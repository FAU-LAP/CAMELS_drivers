# NOMAD-CAMELS driver for Keithley 2400

Driver of the Keithley 2400 source measure unit written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).

## Features

Currently supported are basic voltage and current setting and reading.

## Changes

### 0.1.2

- Fixed bug when the instruments data format was not set to ASCII. Caused errors when reading data ("ascii codec can't decode byte 0x...").
Now automatically sets the data format to ASCII with `:FORM:DATA ASC` at the beginning of every measurement.

## Documentation

For more information and documentation visit the NOMAD-CAMELS [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).