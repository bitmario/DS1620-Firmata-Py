# DS1620-Firmata-Py
Read temperatures from a DS1620 sensor connected to an Arduino using Firmata and Python/pymata-aio

## Contents
Inside the [arduino](arduino/) directory you will find:

* [Libraries](arduino/libraries/) directory with a modified DS1620 library
* [StandardFirmata](arduino/StandardFirmata/StandardFirmata.ino) sketch with DS1620 support in 1SHOT mode
* [StandardFirmataContinuous](arduino/StandardFirmataContinuous/StandardFirmataContinuous.ino) sketch with DS1620 support in continuous mode

The main [python3 script](get_temps.py) serves as an example of how to use Pymata to retrieve the temperature from our custom Firmata.

## Sysex command codes

```
DS1620_CONFIG        = 0x30
DS1620_TEMP          = 0x31
DS1620_TEMP_RESPONSE = 0x32
```

## License

Licensed under the LGPL v2.1, see LICENSE file for details. See included library folders for respective licenses.
