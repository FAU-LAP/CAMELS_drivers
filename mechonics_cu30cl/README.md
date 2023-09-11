# NOMAD-CAMELS Driver for Mechonics CU30CL

Driver of the Mechonics CU30 closed loop piezo controller written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).

## Installation
To use this driver you need the .dll-files provided by mechonics. We do not upload these files to our GitHub. To make sure everything works, copy the files "Servo3AxWrap.dll" and "Servo3AxUSB2.dll"/"Servo3AxUSB2_x64.dll" to the folder of this driver. You can get these files from Mechonics.

## Features
This driver includes a python wrapper for the C-based instrument-dll.  
Positions for all 3 axes may be set and read. The stage's time constant and speed can be set as well.  
The stage-control of NOMAD-CAMELS is fully supported. 

## Documentation

For more information and documentation visit the NOMAD-CAMELS [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).