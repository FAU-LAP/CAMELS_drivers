# NOMAD-CAMELS Driver for NI DAQ Instrument

Driver for a National Instruments DAQ instrument written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/). Comes with a special signal for ophyd-usage. 

## Features
This driver supports usage of up to 8 digital/analog in and outputs of an NI-DAQ instrument.


## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).

## Usage

In `Manage Instruments` set the `line name` to the correct string. Most likely this will be something like `Dev1/ai0` for input channel 1 or `Dev1/ao0` for output channel 1. The `line name` can be found in the NI Measurement & Automation Explorer (NI MAX) software.

## Changes

### 0.1.3

- Fixed broken writing to outputs.


### 0.1.2

Updated a lot of functionality

### 0.1.1

Basic utility for reading inputs and setting outputs