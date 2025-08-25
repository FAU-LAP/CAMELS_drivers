# NOMAD CAMELS driver for a demo source measure unit

Simulated demo source measure unit for testing, written for the measurement software [NOMAD CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).


## Features
This driver can be used to get familiar with the functionalities of NOMAD CAMELS without using an actual instrument / setup.

It is usually used together with the [demo digital multimeter](https://pypi.org/project/nomad-camels-driver-demo-digital-multimeter/).

Both these drivers can communicate with each other.

Two options for this demo are available, that both simulate a semiconductor element on a peltier heater element.
- diode_on_heater: A diode on this heater.
- semiconductor_resistor_on_heater: A simple semiconductor piece on the heater.

This instruments simulates a two-channels source measure unit which is connected as follows:\
- Channel 1 `mesI1, mesV1, setI1, setV1` is connected to the investigated sample (diode or resistor).
- The second channel is connected to the peltier heater and is easiest controlled by using `setI2`, the temperature can be read as a resistance with the demo digital mutlimeter.


## Documentation

For more information and documentation visit the NOMAD CAMELS [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).