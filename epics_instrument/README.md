# NOMAD Camels driver for epics_instrument

Generic driver that allows you to easily implement EPICS PVs in [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/).

You can add PVs by opening the `Manage Instruments` window and simply adding new PVs to the table. This allows you to quickly add or remove PVs from your EPICS instrument and is much easier than writing drivers for each EPICS instrument you want to use in CAMELS.

## In the `Manage Instruments` window

- `PV Short Name` can be anything you want to see and use in CAMELS, for example something like `Hotplate_Temp`
- `PV FUll Name` is the actual PV name in your EPICS system, so probably something like `Cleanroom:Hotplate:Temperature:K`
- Set the PV type to either `read-only` if you **only** want to **read** this PV or change it to `set` if you want to **set** (put/change) **and read** it.


## Changes

### 0.1.1

- Fixed imports and class names: You can now combine multiple types of dynamically created instruments (like EPICS and OPC-UA instruments) in a single measurement.

## Documentation

For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).