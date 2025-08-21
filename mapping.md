# Mapping

As of lakeshore (Python SDK) 1.8.1

GenericInstrument (Base Class) has methods: `connect_usb` and `disconnect_usb`

| LS Method                          | Short Description              | Repo Method             | Endpoint                                          | Note                                          |
| ---------------------------------- | ------------------------------ | ----------------------- | ------------------------------------------------- | --------------------------------------------- |
| **Device Management**              |
| `connect_usb`                      | Connect to USB device          | `connect`               | `POST /api/v1/connect`                            | From GenericInstrument base class             |
| `disconnect_usb`                   | Disconnect from USB device     | `disconnect`            | `POST /api/v1/disconnect`                         | From GenericInstrument base class             |
| `get_identification`               | Get device identification info | `get_identification`    | `GET /api/v1/identification`                      | Returns manufacturer, model, serial, firmware |
| `get_channel_reading_status`       | Get channel status flags       | `get_status`            | `GET /api/v1/{channel}/status`                    | Returns bit status dictionary                 |
| `set_modname`                      | Set module name                | `set_modname`           | `POST /api/v1/module_name`                        | Names the module                              |
| `get_modname`                      | Get module name                | `get_modname`           | `GET /api/v1/module_name`                         | Returns module name                           |
| `set_brightness`                   | Set display brightness         | `set_brightness`        | `POST /api/v1/brightness`                         | 0-100 percent                                 |
| `get_brightness`                   | Get display brightness         | `get_brightness`        | `GET /api/v1/brightness`                          | Returns brightness level (0-100)              |
| **Temperature Readings**           |
| `get_celsius_reading`              | Get temperature in Celsius     | `get_monitor`           | `GET /api/v1/{channel}`                           | Part of monitor response                      |
| `get_fahrenheit_reading`           | Get temperature in Fahrenheit  | `get_monitor`           | `GET /api/v1/{channel}`                           | Part of monitor response                      |
| `get_kelvin_reading`               | Get temperature in Kelvin      | `get_monitor`           | `GET /api/v1/{channel}`                           | Part of monitor response                      |
| `get_sensor_reading`               | Get raw sensor reading         | `get_monitor`           | `GET /api/v1/{channel}`                           | Part of monitor response                      |
| **Input Configuration**            |
| `get_input_parameter`              | Get input channel parameters   | `get_input_parameter`   | `GET /api/v1/input/{channel}`                     | Returns InputParameter object                 |
| `set_input_parameter`              | Set input channel parameters   | `set_input_config`      | `POST /api/v1/input/{channel}`                    | Accepts InputParameter object                 |
| `get_sensor_name`                  | Get sensor channel name        | `get_input_parameter`   | `GET /api/v1/input/{channel}`                     | Included in InputParameter response           |
| `set_sensor_name`                  | Set sensor channel name        | `set_input_config`      | `POST /api/v1/input/{channel}`                    | Part of InputParameter                        |
| `get_filter`                       | Get channel filter parameter   | `get_input_parameter`   | `GET /api/v1/input/{channel}`                     | Included in InputParameter response           |
| `set_filter`                       | Set channel filter parameter   | `set_input_config`      | `POST /api/v1/input/{channel}`                    | Part of InputParameter                        |
| **Curve Management**               |
| `get_curve_header`                 | Get curve header parameters    | `get_curve_header`      | `GET /api/v1/curve/{channel}/header`              | Returns CurveHeader object                    |
| `set_curve_header`                 | Set curve header parameters    | `set_curve_header`      | `POST /api/v1/curve/{channel}/header`             | Accepts CurveHeader object                    |
| `get_curve_data_point`             | Get single curve data point    | `get_curve_data_point`  | `GET /api/v1/curve/{channel}/data-point/{index}`  | Returns CurveDataPoint                        |
| `set_curve_data_point`             | Set single curve data point    | `set_curve_data_point`  | `POST /api/v1/curve/{channel}/data-point/{index}` | Accepts CurveDataPoint                        |
| -                                  | Get all curve data points      | `get_curve_data_points` | `GET /api/v1/curve/{channel}/data-points`         | Custom endpoint returning all 200 points      |
| `delete_curve`                     | Delete user curve              | -                       | -                                                 | Not implemented                               |
| **PROFIBUS (Not Implemented)**     |
| `set_profibus_address`             | Set PROFIBUS address           | -                       | -                                                 | Not implemented                               |
| `get_profibus_address`             | Get PROFIBUS address           | -                       | -                                                 | Not implemented                               |
| `set_profibus_slot_count`          | Set PROFIBUS slot count        | -                       | -                                                 | Not implemented                               |
| `get_profibus_slot_count`          | Get PROFIBUS slot count        | -                       | -                                                 | Not implemented                               |
| `set_profibus_slot_configuration`  | Configure PROFIBUS slot        | -                       | -                                                 | Not implemented                               |
| `get_profibus_slot_configuration`  | Get PROFIBUS slot config       | -                       | -                                                 | Not implemented                               |
| `get_profibus_connection_status`   | Get PROFIBUS connection status | -                       | -                                                 | Not implemented                               |
| **Sensor Units Reading**           |
| `get_sensor_units_channel_reading` | Get sensor units value         | -                       | -                                                 | Duplicate of `get_sensor_reading`             |
| **Factory Reset**                  |
| `set_factory_defaults`             | Reset to factory defaults      | -                       | -                                                 | Not implemented                               |
