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
![M5 CoreInk Analog Clock NTP.jpg](img/M5%20CoreInk%20Analog%20Clock%20NTP_250px.jpg)
![M5 CoreInk Analog Clock NTP Code Example.png](img/M5%20CoreInk%20Analog%20Clock%20NTP%20Code%20Example.png)