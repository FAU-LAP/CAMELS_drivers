# NOMAD Camels driver for derived hannels

This is a special driver for [NOMAD CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/).
It can be used to directly calculate values from other channels inside CAMELS.


## How to use

You may add an arbitrary number of channels to each instance of this instrument.
Each channel can be configured either as readable or writable.

When you make the channel readable, you need to select which channels it depends on. The calculation formula should then depend on these channels.

A writable channel may only write to a single channel. The calculation formula is then, how the output is scaled. In that case, use `x` for the value written to the newly defined channel. For example when you want to define a new channel `scaled` that writes to the channel `channel1` of some instrument, you can write `x * 5` so when `scaled` is set to `2`, `channel1` will be set to `10`.

Alternatively, you can define a python function inside any file and select "From File" for the conversion (either read or write). Then select the file and set the name of the function that should be used for the conversion.
- For writing: The function may take only one argument (which will be the set value) and should return one value.
- For reading: Make sure that the function takes the read channels as arguments, for example:
```python
def read_conversion(read_channel_1, read_channel_2):
    return read_channel_1 + read_channel_2
```
or
```python
def read_conversion(**values):
    return values['read_channel_1'] + values['read_channel_2']
```


## Documentation

For more information on NOMAD CAMELS and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).


## Changelog

### 0.1.3
Made custom python functions more robust when the file is removed

### 0.1.2
Added functionality to use custom python functions.