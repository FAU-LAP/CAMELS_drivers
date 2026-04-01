# NOMAD-CAMELS Driver for Voltcraft PPS

Driver for communicating with a Agilent E363X series power supply written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).

## Features
Set voltage and current limit for up to all three channels.

## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).

## Changes

### 0.1.2

- Renamed the channels from `1,2,3` to `P25V, N25V, P6V` to reflect the actual channels of the power supply.
- Now has a single `output` Channel that turns **all** channels on (send `1`) or off (send `0`).

### 0.1.1

- Changed it so that all current outputs are regular `Set Channels` and not `Configure Channels`. This means you always need to set both the current and voltage value for each channel. The power supply will output until either the voltage or current limit is reached. Renamed the channels to `current_1` and not `current_limit_1` to reflect this change.


### 0.1.0

Basic functionality.