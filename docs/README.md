# Plant Monitor

## Introduction

This document provides information about requirements and instructions how to use and configure Simple Plant Monitor. 

Device is based on  Raspberry Pi Pico. The device might be equipped with sensors for air humidity, temperature, plant moisture, and light intensity. 
It will have a modular design, allowing multiple humidity sensors for plants or photoresistors to be connected. 

The entire system is based on the MQTT protocol, enabling it to share information with other devices (like phone). Advising to use HiveMq free cloud solution.

Device is using a microUSB port as a power supply.

The system is designed to be highly modular, allowing easy addition of new sensors with appropriate drivers.

Source Code: Plant Monitor.

Required elements to build device:
- 1 Raspberry Pi Pico W
- 1 ADC Multiplexer
- microUSB Cable

Optional elements (some of the devices can be configured multiple times):
- dht11 sensor
- moisture sensor
- fotoresistor

## Configuration

All configuration `jsons` have to be placed in the configuration folder.

Current configuration `jsons`:
- `connection.json` - informations required to connect with wifi
- `mqtt.json` - informations required to connect with mqtt server
- `accessors.json` - list of adc multiplexers to use
- `devices.json` - list of devices to use

### `connection.json`

We have to provide information required to connect with out wifi. Option none will not connect with wifi. 

```
{
  "type": "wifi/none",
  "ssid": "your_ssid",
  "password": "your_password",
  "maxConnectionTime": 15
}
```

### `mqtt.json`

Informations requirted to connec with mqtt broker, advicsed is to use free Cloud broker [HiveMq](https://www.hivemq.com/).

```
{
  "type" : "hivemq/none",
  "server": "your_mqtt_server",
  "port": 8883,
  "client": "your_client_id",
  "ssl": true,
  "keepAlive": 60,
  "authentication":
  {
    "type": "user&password",
    "data":
    {
      "username": "your_mqtt_user",
      "password": "your_mqtt_password"
    }
  },
  "typeSpecificData":
  {
    "baseTopic": "plantMonitor/"
  }
}
```

### `accessors.json`

Accessors are list of ADC multiplexers each multpilexer is recognized by `id` it is also used to bind between multiplexer and device.
Pins are bytes in order 0,1,2,3.
```
[
  {
    "id": "1",
    "type": "HP4067",
    "slots": 16,
    "pins": [12, 13, 14, 15],
    "adcPin": 26
  }
]
```

### `devices.json`

List of devices that are recognized by id.

```
[
    {
        "id": "1",
        "type": "air",
        "name": "dht11",
        "ground": 38,
        "vcc": 36,
        "availability": {
            "enabled": true,
            "topic": "availability"
        },
        "data":
        {
            "loopSpanMs": 500,
            "pin": 1,
            "temperature":
            {
                "unit": "Celsius",
                "topic": "temperature",
                "unitTopic": "unit",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 0.2,
                    "minimalIntervalSeconds": 20
                }
            },
            "humidity":
            {
                "unit": "Percentage",
                "topic": "humidity",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 1,
                    "minimalIntervalSeconds": 20
                }
            }
        }
    }
]
```

## Sub Devices

List of device task and devices supported with drivers.

### Multiplexers

Type recognizes device.

Example Devices:
- [HP4067](https://pl.aliexpress.com/item/1005004954660613.html?src=google&src=google&albch=shopping&acnt=708-803-3821&slnk=&plac=&mtctp=&albbt=Google_7_shopping&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&albcp=19735245762&albag=&trgt=&crea=pl1005004954660613&netw=x&device=c&albpg=&albpd=pl1005004954660613&gad_source=1&gclid=CjwKCAjw57exBhAsEiwAaIxaZrnzK7EP3tdbqN-khqhh3gij5LT1AIEcblLT9bxBaDc57qDIqqHX2RoC_vAQAvD_BwE&gclsrc=aw.ds&aff_fcid=b84a5231311343219ab59db056dede5b-1714318309518-06954-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=b84a5231311343219ab59db056dede5b-1714318309518-06954-UneMJZVf&terminal_id=34dda35e48bc427cb9f5407905e202d9&afSmartRedirect=y) - 16 channel adc multiplexer

Maximal number of sensors: 1.

Slots is number of adc multiplexers.

```
[
  {
    "id": "1",
    "type": "HP4067",
    "slots": 16,
    "pins": [12, 13, 14, 15],
    "adcPin": 26
  }
]
```

### Temperature and Moisture Sensor

Type of this devices is `air`. Device measures air humidity and temperature. 

Example Devices:
- [dht11](https://pl.aliexpress.com/item/1005005553381999.html?src=google&src=google&albch=shopping&acnt=708-803-3821&slnk=&plac=&mtctp=&albbt=Google_7_shopping&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&albcp=19735245762&albag=&trgt=&crea=pl1005005553381999&netw=x&device=c&albpg=&albpd=pl1005005553381999&gad_source=1&gclid=CjwKCAjw57exBhAsEiwAaIxaZsElzOfCpgnb9v_VKIIexVC-L50T9nH2ne481vd9yKF7nowZAasBEBoCoYgQAvD_BwE&gclsrc=aw.ds&aff_fcid=1f23f14340bd4063af63aa6ef7a645cc-1714318490652-04579-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=1f23f14340bd4063af63aa6ef7a645cc-1714318490652-04579-UneMJZVf&terminal_id=34dda35e48bc427cb9f5407905e202d9&afSmartRedirect=y) 

Maximal number of sensors: 1.

#### Features

Base topic: `{base_device_topic}/air/{device_name}/{device_id}` example `plantMonitor/air/dht11/1`

##### Availability

Feature task is to stop / start measurments on device.

Topic: `{base_device_topic}/air/{device_name}/{device_id}/{availability:topic}` example `plantMonitor/air/dht11/1/availability`

Example payload:
```
{
    "value": "on"
}
```

##### Temperature

Feature is to informa about temperature for plant/plants. In configured example temperature will be send once per 20 seconds if there will be any changes.

Topic: `{base_device_topic}/air/{device_name}/{device_id}/{data:temperature:topic}` example `plantMonitor/air/dht11/1/temperature`

Example received payload:
```
{
    "time": 1714315868, 
    "timeUnit": "s", 
    "value": 21, 
    "unit": "Celsius"
}
```

##### Temperature Unit

Feature is to adjust unit for temperature returend by device. (Temperature will be converted to right unit)

Topic: `{base_device_topic}/air/{device_name}/{device_id}/{data:temperature:topic}/{data:temperature:unitTopic}` example `plantMonitor/air/dht11/1/temperature/unit`

Example push payload:
```
{
    "unit": "F"
}
```

##### Air Humidity

Feature is to informa about humidity for plant/plants. In configured example humidity will be send once per 20 seconds if there will be any changes.

Topic: `{base_device_topic}/air/{device_name}/{device_id}/{data:humidity:topic}` example `plantMonitor/air/dht11/1/humidity`

Example received payload:
```
{
    "time": 1714315868, 
    "timeUnit": "s", 
    "value": 21, 
    "unit": "Percentage"
}
```

#### Example configuration

```
[
    {
        "id": "1",
        "type": "air",
        "name": "dht11",
        "ground": 38,
        "vcc": 36,
        "availability": {
            "enabled": true,
            "topic": "availability"
        },
        "data":
        {
            "loopSpanMs": 500,
            "pin": 16,
            "temperature":
            {
                "unit": "Celsius",
                "topic": "temperature",
                "unitTopic": "unit",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 0.2,
                    "minimalIntervalSeconds": 4
                }
            },
            "humidity":
            {
                "unit": "Percentage",
                "topic": "humidity",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 1,
                    "minimalIntervalSeconds": 4
                }
            }
        }
    }
]
```

### Soil Moisture Sensors

Type of this devices is `soil`.

Example Devices:
- [sms](https://botland.com.pl/czujniki-wilgotnosci/1588-czujnik-wilgotnosci-gleby-5904422368289.html?cd=20567593583&ad=&kd=&gad_source=1&gclid=CjwKCAjw57exBhAsEiwAaIxaZldpUD3XtGK59sf4WO1Q5dNLYWhV7JpSTajF_JeflWHCq7v0MHvKsxoC8sQQAvD_BwE) 
- [CSMSV1](https://botland.com.pl/gravity-czujniki-pogodowe/10305-dfrobot-gravity-analogowy-czujnik-wilgotnosci-gleby-odporny-na-korozje-sen0193-6959420910434.html?cd=20567593583&ad=&kd=&gad_source=1&gclid=CjwKCAjw57exBhAsEiwAaIxaZuq-jqT9MRCe9ytQmkxCBVGU5aVK3k3RzuxumnmlA7rEEFGsiIh_1xoCkPgQAvD_BwE) 

Maximal number of sensors: depends on adc multiplexer.

#### Features

##### Availability

Feature task is to stop / start measurments on device.

Topic: `{base_device_topic}/soil/{device_name}/{device_id}/{availability:topic}` example `plantMonitor/soil/sms/2/availability`

Example payload:
```
{
    "value": "on"
}
```

##### Moisture

Feture returns information about plant moisture.

Topic: `{base_device_topic}/soil/{device_name}/{device_id}/{data:temperature:topic}` example `plantMonitor/soil/sms/2/moisture`

Example received payload:
```
{
    "time": 1714315868, 
    "timeUnit": "s", 
    "value": 21, 
    "unit": "Percentage"
}
```

#### Example Configuration


***Note: It is worth to use bigger interval and treshold for cheap sms sensors due to measurments fluctuations.***

```
[
    {
        "id": "2",
        "type": "soil",
        "name": "sms",
        "ground": 38,
        "vcc": 36,
        "availability": {
            "enabled": true,
            "topic": "availability"
        },
        "data":
        {
            "loopSpanMs": 500,
            "mux_id": 1,
            "channel": 1,
            "moisture":
            {
                "unit": "Percentage",
                "topic": "moisture",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 5,
                    "minimalIntervalSeconds": 5
                }
            }
        }
    },
    {
        "id": "3",
        "type": "soil",
        "name": "gravity_v1",
        "ground": 38,
        "vcc": 36,
        "availability": {
            "enabled": true,
            "topic": "availability"
        },
        "data":
        {
            "loopSpanMs": 500,
            "mux_id": 1,
            "channel": 15,
            "moisture":
            {
                "unit": "Percentage",
                "topic": "moisture",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 1,
                    "minimalIntervalSeconds": 5
                }
            }
        }
    }
]
```

### Insolation Sensors

Type of this devices is `light`.

Example Devices:
- [is](https://botland.com.pl/czujniki-swiatla-i-koloru/16560-czujnik-swiatla-ldr-rezystancyjny-dla-arduino-okystar-5904422378202.html) 

Maximal number of sensors: 1.

#### Features

##### Availability

Feature task is to stop / start measurments on device.

Topic: `{base_device_topic}/light/{device_name}/{device_id}/{availability:topic}` example `plantMonitor/light/is/1/availability`

Example payload:
```
{
    "value": "on"
}
```

##### Insolation

Feture returns information about insolation.

Topic: `{base_device_topic}/light/{device_name}/{device_id}/{data:temperature:topic}` example `plantMonitor/light/is/1/insolation`

Example received payload:
```
{
    "time": 1714315868, 
    "timeUnit": "s", 
    "value": 21, 
    "unit": "Percentage"
}
```

#### Example Configuration

In contrast to sms sensors this sensor should be on separate adc pin (raspberry pi pico w has 2 so there is no problem).

```
[
    {
        "id": "4",
        "type": "light",
        "name": "is",
        "ground": 38,
        "vcc": 36,
        "availability": {
            "enabled": true,
            "topic": "availability"
        },
        "data":
        {
            "loopSpanMs": 500,
            "adcPin": 27,
            "insolation":
            {
                "unit": "Percentage",
                "topic": "insolation",
                "sendAsJson": true,
                "threshold":{
                    "type": "value",
                    "value": 4,
                    "minimalIntervalSeconds": 5
                }
            }
        }
    }
]
```

### 3D Model

3D model can be found at [thingiverse Plant Monitor]().

### Example of wiring schema

Example schema introduces device configuration for retriving key informations about single plant.

Involved devices:
- dht11 sensor
- adc multiplexer (other pins than in example configuration)
- one SMS sensor
- insolation sensor

![wiring](./BasicSchematic.png)

### Setup

1. Place contents of `src` folder in raspbery pi pico w.
2. Provide `wifi` configuration.
3. Provide `mqtt` configuration (you can use [HiveMq](https://auth.hivemq.cloud/) as a cloud broker).
4. Provide `devices` and `accessors` configurations.
5. You can run project using thonny in order to test working.
6. Finaly device will run when connecting to power source.

If you want to see console logging change:

`logger = FileLogger(console=False, debug=False)`

to

`logger = FileLogger(console=True, debug=False)`

### Contribution / Development

#### New Device Type

In order to add new device type (for example rain sernsors) we should create new folder in `src/features/devices` with name as category of devices.
Then we have to prepare class that will implement `Device` class also we should be aware to implement default driver for this category.
(When we have 2 devices that communicate with different protocols we may want to create a sperate class that implements `Device`)
Finally we have to add our device type to `device_factory.py`.

#### New Device For Existing Device Type

A. Differend communication model
In order to add new device model (example dht22) we navigate to device category (`src/features/devices/air`), inside category folder we should provide new implementation of `Device` class with apporoperiet driver.

B. Same communuication model

When devices uses similar communication model we can only provide driver for sepcific modules. 
You can find example in `src/features/devices/soil_humidity`.

#### Accessing other devices data

This can be done via Mqtt implementation clas via `get_values` method, we just have to know topics of the devices / or how topic starts and then we can access whole group of devices (`get_values("{base_device_topic}/soil")` will return all informations that are send by soil moisture sensors)