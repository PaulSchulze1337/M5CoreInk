# M5 Core Ink - Analog Clock with NTP Sync and Daylight Saving Time (DST) Support

## Overview
- Clock is synchronized with NTP server
- Daylight saving time (DST) support via hard coded JSON file (see [dayLightSavingTimes.json](dayLightSavingTimes.json))

## Sources
- [Source Code (UI Flow V1)](Analog_Clock_Sketch.m5f)
- [Daylight Saving Times (JSON)](dayLightSavingTimes.json)

## Instructions
1. Load the [UI Flow Source Code](Analog_Clock_Sketch.m5f) using UI Flow V1 (see [M5Stack UI Flow](https://flow.m5stack.com/))
2. Connect M5 CoreInk using API Key 
1. Modify WiFi SSID and Password in the sketch
1. Upload the sketch to the M5 CoreInk


## Enable USB/Serial Port Terminal
- Install minicom for Linux:Ubuntu
``` bash
  sudo apt-get install minicom
```

- Connect M5 CoreInk to USB port an run the following command to find the tty
``` bash
  sudo dmesg | grep tty
```

- Run minicom with the following command
``` bash
  sudo minicom -b 115200 -o -D /dev/ttyACM0
```


## Pictures
![Analog Clock_250px.jpg](img/Analog%20Clock_250px.jpg)
![Code Example.png](img/Code%20Example.png)