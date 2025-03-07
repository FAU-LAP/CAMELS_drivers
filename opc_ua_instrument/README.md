# NOMAD Camels driver for opc_ua_instrument

Driver for opc_ua_instrument written for the measurement software [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/).

Allows you to add OPC UA variables that already exist.

Add the URL of the server hosting your variables. Similar to 

```
opc.tcp://localhost:4840/freeopcua/server/
```

Add the namespace URL. For example

```
http://examples.freeopcua.github.io
```
You can now add any number of variables by clicking the green `+` symbol. 

Select if you want to be able to change (`set`) them or if you only want to read (`read-only`) the variables with the drop-down menu.

The variable is accessed using its browse path and should look something like this:

```
0:Objects/2:MyObject/2:MyVariable
```

## Changes

### 0.1.5

- Fixed imports and class names: You can now combine multiple types of dynamically created instruments (like EPICS and OPC-UA instruments) in a single measurement.

### 0.1.4.

- Fixed data writing to the variables to always use the correct `ua.DataType`

### 0.1.3

- Fixed broken dependencies.

### 0.1.2

- When setting (writing) to variables the data-type of the variable is always checked and the value is cast to this data type before setting. Should make writing to variables much more stable.

### 0.1.1

- Added automatic variable adding. For this enter a RegEx pattern in the text field next to the `Fetch and Add` button. Then press the `Fetch and Add` button.
This will go through the given server and try to match either the Node-ID or the Browse Path with the RegEx pattern given. Matches will be added with their Browse Path into the list below.

   > [!WARNING]
   > This can take quite some time if there are many nodes in the server!

Make sure to give them custom names under `Name` before clicking "OK".

## Documentation

For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).