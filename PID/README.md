# NOMAD-CAMELS Driver for PID

This package provides everything to run a PID Controller written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).\
This PID is implemented as a pure software PID and can take any channel as input and any channel as output. 

## How to use
Use the `input channel` to control the PID values. After calculating the output, it will be written to the `output channel`.

The `bias channel` is for example useful in systems that consist of heating and cooling for temperature control. This channel is set to certain fixed values depending on the setpoint (see below).

The conversion functions for reading / setting work as follows:\
The value from the `input channel` is the input for the conversion function for reading. Two default functions come with this package: `Pt1000` and `Pt100`, referring to the temperature sensitive resistors with the same name. These functions calculate the temperature from a measured resistance, i.e. when your `input channel` is a resistance, you may use one of these functions to make your PID control a temperature.

The `time delta` is the time between to PID steps (i.e. reading, calculating, setting the new output value).

The PID values are set with the table:\
- **setpoint**: When your desired setpoint is above this value, that line of the table will be used for the PID values.
- **kp, ki, kd**: These are the typical three values for the proportional, integral and derivative part of the PID.
- **max_value, min_value**: These values limit the output range.
- **bias**: This value is put to the `bias channel` if that channel is provided.
- **stability-delta, stability-time**: When the value is in the range of *stability-delta* around the setpoint for *stability-time* seconds, the PID will set its channel `pid_stable` to `True`. This is also used in the *PID wait for stable* step.

When `interpolate PID values` is used, all values inside the table are interpolated column-wise between two setpoints.\
Example: When you provide `kp=1` for the setpoint `0.0` and `kp=2` for the setpoint `10.0`, using a setpoint of `5.0` in the PID will set `kp` to `1.5`.

The instruments comes with a custom step used in protocols: "**PID wait for stable**". This step provides a convenience function to wait until the stability criteria of the PID are fulfilled.

#### Ramping
When turning on the ramping function, the PID will use the values `ramp_to` and `ramp_speed` to change the setpoint with each PID step according to the `ramp_speed` until the setpoint reaches the value of `ramp_to`.

The ramp will start at the setpoint that is set when the ramping starts. When stopped before reaching the desired value, it will stay at the current setpoint.


## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).


## Changelog

### 0.3.1
Fixed:
- Broken updating of PID settings fixed.

### 0.3.0
Added functionality to ramp the PID setpoint.

### 0.2.3
Improvements:
- Made description in Readme clearer
- UI for custom conversion functions cleaner


### 0.2.2
Improvements:
- Now allowing for custom conversion functions and from user-defined python files
- Added descriptions for PID-channels and configs

Fixes:
- When startup of manual control breaks, no additional error is raised on closing anymore

### 0.2.1
Fixes:
- settings got broken in last update, now fixed
- progress bar of waiting step now works

## 0.2.0
Changes:
- many previous settings are now configs, allowing for better access to the PID while running

Fixes:
- NaN values are now handled by turning off the PID for the moment, instead of crashing

### 0.1.10
Fixes:
- Output and single pid values should now be correctly recorded as float