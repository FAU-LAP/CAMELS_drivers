# NOMAD-CAMELS Driver for PyLabLibs Cam-Control 

Connects to the server of Cam-Control to save, snap and request frames. Written for the measurement software [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).


## Documentation
The backbone of this driver is the cam-control software by [PyLabLib](https://pylablib-cam-control.readthedocs.io/). The software must be running and set up to [allow server communication](https://pylablib-cam-control.readthedocs.io/en/latest/expanding.html#control-server).
CAMELS then connects to the server and sends requests to the server. You must set up cam-control via its own GUI and you can then use CAMELS to actually save images with the exact settings from the GUI.
Currently you can set the exposure time, save snapshots locally and save continuous frames locally as well as save frames into the HDF5 files of CAMELS. You can also save the background image which is currently being subtracted. The direct saving of frames to HDF5 files is quite slow as the server takes some time to answer (about 1 second per frame even for low exposure times of < 100 ms).


For more information and documentation visit our [GitHub.io](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html) page.