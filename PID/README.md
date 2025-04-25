# NOMAD-CAMELS Driver for PID

This package provides everything to run a PID Controller written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).\
This PID is implemented as a pure software PID and can take any channel as input and any channel as output. 


## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).


## Changelog

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