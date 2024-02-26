# NOMAD-CAMELS Driver for PyLabLibs Cam-Control 

Connects to the server of Cam-Control to save, snap and request frames. Written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).

More information on how to use it can be found [here](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/cam_control_pylablib/cam_control_pylablib.html)

## Changelog

### 0.1.4

- Improved frame acquisition. Increased speed and made it more stable.

### 0.1.3

- Changed `grab_background` to wait for the background to be grabbed before continuing.
- Changed `get_single_frame` and `get_background_frame` to wait for the frames to actually be available and then read them.
- Added device setting that allows you to choose if you want to overwrite the exposure time set in the GUI.

### 0.1.2

- Removed `read_wait` as it is no longer needed.
- Changed the end of the file name when using suffixes to be `time.time()` and not `datetime.date.today()`

### 0.1.1

Optimized reading of frames into python. Drastically increased reading speed.

### 0.1.0

Core functions. Not optimized.

## Documentation

The backbone of this driver is the cam-control software by [PyLabLib](https://pylablib-cam-control.readthedocs.io/). The software must be running and set up to [allow server communication](https://pylablib-cam-control.readthedocs.io/en/latest/expanding.html#control-server).
CAMELS then connects to the server and sends requests to the server. You must set up cam-control via its own GUI and you can then use CAMELS to actually save images with the exact settings from the GUI.
Currently you can set the exposure time, save snapshots locally and save continuous frames locally as well as save frames into the HDF5 files of CAMELS. You can also save the background image which is currently being subtracted. The direct saving of frames to HDF5 files is quite slow as the server takes some time to answer (about 1 second per frame even for low exposure times of < 100 ms).

For more information and documentation visit our [GitHub.io](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html) page.