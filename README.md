# dbus-imt-si-rs485tc

Driver for the [imt-si-rs485tc Solar Irradiance Sensor](https://www.imt-solar.com/products/solar-irradiance-sensor/si-sensor/).  

  

A separate _USB to RS485_ converter cable is required for each sensor. The driver works with the factory settings of the sensor. No manual configuration required.  
  

The sensor measures 
* Solar Irradiance [W/m2]
* Temperature [°C]
* Wind Speed [m/s], _optional_
* External Temperature [°C], _optional_

The _optional_ measurements are only available if the corresponding subsensor is attached.
The measurements are published on DBus under the service
`com.victronenergy.meteo.ttyUSBx`

The object paths of the measurements are
```
/Irradiance
/WindSpeed
/CellTemperature
/ExternalTemperature
```


Optional measurements are only published on DBus after a non zero value has be measured at least once.

