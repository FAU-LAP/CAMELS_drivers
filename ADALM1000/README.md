# NOMAD Camels driver for ADALM1000

Driver for ADALM1000 written for the measurement software [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/). 

Requires the correct drivers. Download and install the latest version from the manufacturers [GitHub](https://github.com/analogdevicesinc/libsmu/releases).

```{caution}
Drivers only work for Python versions <= 3.10.9 !
CAMELS is often installed using Python 3.11. You therefore might need to downgrade your Python version.
```

Also requires the `pysmu` package. Install via

```bash
pip install -i https://test.pypi.org/simple/ pysmu
```

## Documentation

For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html).