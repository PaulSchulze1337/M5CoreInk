# This is the microPython code for the Analog Clock Sketch

from m5stack import *
from m5ui import *
from uiflow import *
import network
import wifiCfg
import ntptime
import json

import time


setScreenColor(lcd.WHITE)


setActive = None
weekdayNumber = None
valueAsNumber = None
deg = None
len2 = None
x = None
weekdayString = None
y = None
year = None
month = None
day = None
hour = None
valueAsString = None
calculatedXValue = None
calculatedYValue = None
DEBUG = None
newTimeReceivedFromNTP = None
degHourHand = None
currentDegree = None
currentTime = None
fixedHour = None
enableDayLightSaving = None
TimeZone = None
degMinuteHand = None
dayLightSavingJson = None
WiFiSSID = None
WiFiPwd = None
currentStartEnd = None
dayLightSavingStartDay = None
dayLightSavingEndDay = None



circle0 = M5Circle(100, 100, 4, lcd.BLACK, lcd.BLACK)
label_weekday = M5TextBox(78, 117, "Day", lcd.FONT_UNICODE, lcd.BLACK, rotate=0)
label_clock = M5TextBox(63, 63, "00:00", lcd.FONT_DejaVu24, lcd.BLACK, rotate=0)
label_day = M5TextBox(154, 182, "11-11", lcd.FONT_Default, lcd.BLACK, rotate=0)
label03 = M5TextBox(172, 90, "3", lcd.FONT_DejaVu18, lcd.BLACK, rotate=0)
hour_t = M5Line(M5Line.PLINE, 100, 100, 100, 100, lcd.BLACK)
label12 = M5TextBox(90, 22, "12", lcd.FONT_DejaVu18, lcd.BLACK, rotate=0)
label06 = M5TextBox(93, 165, "6", lcd.FONT_DejaVu18, lcd.BLACK, rotate=0)
label_year = M5TextBox(0, 182, "2021", lcd.FONT_Default, lcd.BLACK, rotate=0)
minute_t = M5Line(M5Line.PLINE, 98, 96, 173, 96, lcd.BLACK)
label09 = M5TextBox(18, 90, "9", lcd.FONT_DejaVu18, lcd.BLACK, rotate=0)

import math


# Enables/Disalbes Wifi
def toogleWiFi(setActive):
  global weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  if setActive:
    if not (wifiCfg.wlan_sta.isconnected()):
      print("Enable WiFi Module")
      wlan.active(True)
      while not (wifiCfg.wlan_sta.isconnected()):
        wifiCfg.doConnect(WiFiSSID, WiFiPwd)
        wait_ms(500)
    print("WiFi is already connected.")
  else:
    print("Disable WiFi Module")
    wlan.disconnect()
    wlan.active(False)

# Change labels, if you wish a different localization.
def convertToLocale(weekdayNumber):
  global setActive, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  weekdayString = ''
  if weekdayNumber==0:
    weekdayString = 'So'
  elif weekdayNumber==1:
    weekdayString = 'Mo'
  elif weekdayNumber==2:
    weekdayString = 'Di'
  elif weekdayNumber==3:
    weekdayString = 'Mi'
  elif weekdayNumber==4:
    weekdayString = 'Do'
  elif weekdayNumber==5:
    weekdayString = 'Fr'
  elif weekdayNumber==6:
    weekdayString = 'Sa'
  else:
    print("Error: Day not known. Fallback to --")
    weekdayString = '--'
  return weekdayString

# Describe this function...
def addHeadingZeroToNumber(valueAsNumber):
  global setActive, weekdayNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  valueAsString = str(valueAsNumber)
  if len(valueAsString) == 1:
    valueAsString = (str('0') + str(str(valueAsNumber)))
  return valueAsString

# Describe this function...
def calculateXValue(deg, len2, x):
  global setActive, weekdayNumber, valueAsNumber, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  calculatedXValue = math.cos((float(deg) + -90) / 180.0 * math.pi) * float(len2) + float(x)
  return int(calculatedXValue)

# We need to convert the given weekday string into a number to setup the RTC
def convertWeekdayToNumber(weekdayString):
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  weekdayNumber = 0
  print("[convertWeekdayToNumber]: convert weekday: " + weekdayString + " to a number: 0-6")
  if weekdayString=='Sun':
    weekdayNumber = 0
  elif weekdayString=='Mon':
    weekdayNumber = 1
  elif weekdayString=='Tue':
    weekdayNumber = 2
  elif weekdayString=='Tues':
    weekdayNumber = 2
  elif weekdayString=='Wed':
    weekdayNumber = 3
  elif weekdayString=='Thu':
    weekdayNumber = 4
  elif weekdayString=='Thur':
    weekdayNumber = 4
  elif weekdayString=='Fri':
    weekdayNumber = 5
  elif weekdayString=='Sat':
    weekdayNumber = 6
  else:
    print("[convertWeekdayToNumber]: Error: Day not known: " + weekdayString)
    weekdayNumber = 99
  return weekdayNumber

# Describe this function...
def calculateYValue(deg, len2, y):
  global setActive, weekdayNumber, valueAsNumber, x, weekdayString, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  calculatedYValue = math.sin((float(deg) + -90) / 180.0 * math.pi) * float(len2) + float(y)
  return int(calculatedYValue)

# Describe this function...
def updateAndDrawClockFace():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  print("updateAndDrawClockFace called...")
  print("Clear LCD!")
  clearDisplay()
  updateHandsOfAnalogClockFace()
  drawStaticAnalogClockFace()
  updateDigitalClockFace()
  print("Write LCD!")
  # draw everthing
  coreInkShow()

# Describe this function...
def updateRTCwithDateTimeFromNTP():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  toogleWiFi(True)
  newTimeReceivedFromNTP = False
  try :
    print("[updateRTCwithDateTimeFromNTP]: Try: Init time from NTP.")
    ntp = ntptime.client(host='de.pool.ntp.org', timezone=TimeZone)
    print("[updateRTCwithDateTimeFromNTP]: Time received from NTP.")
    newTimeReceivedFromNTP = True
    pass
  except:
    print("[updateRTCwithDateTimeFromNTP]: Catch: failed to get time from ntp")
  if not DEBUG:
    toogleWiFi(False)
  if newTimeReceivedFromNTP:
    print("[updateRTCwithDateTimeFromNTP]: Time from NTP was updated. Update RTC...")
    print("[updateRTCwithDateTimeFromNTP]: Set RTC...")
    # Due to a miracle this function is returning Strings of "Sun, Mon, ..." instead of numbers.
    # To simplify:
    # Adjustment of daylight saving time is done, when clock is syncing with NTP.
    rtc.set_datetime(((ntp.year()), (ntp.month()), (ntp.day()), convertWeekdayToNumber(ntp.weekday()), adjustDayLightSaving(int((ntp.year())), int((ntp.month())), int((ntp.day())), int((ntp.hour()))), (ntp.minute()), (ntp.second())))
    print("[updateRTCwithDateTimeFromNTP]: RTC was set successfully updated.")
  print("[updateRTCwithDateTimeFromNTP]: finished")

# Describe this function...
def clearDisplay():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  lcd.clear()
  label_weekday.setText('    ')
  label_clock.setText('     ')
  label_year.setText('    ')
  label_day.setText('     ')
  label03.setText('  ')
  label06.setText('  ')
  label09.setText('  ')
  label12.setText('  ')

# Describe this function...
def updateHandsOfAnalogClockFace():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  print("updateHandsOfAnalogClockFace called...")
  degHourHand = (rtc.datetime()[4]) * 30 + float((rtc.datetime()[5])) / 2
  hour_t.setSize(100, 100, calculateXValue(degHourHand, 50, 100), calculateYValue(degHourHand, 50, 100))
  degMinuteHand = (rtc.datetime()[5]) * 6
  minute_t.setSize(100, 100, calculateXValue(degMinuteHand, 95, 100), calculateYValue(degMinuteHand, 95, 100))

# Describe this function...
def drawStaticAnalogClockFace():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  print("drawStaticAnalogClockFace called...")
  # draw lines every 1 minutes on the clock face.
  # 1 Minute is every 5 degree.
  for currentDegree in range(0, 355, 6):
    lcd.line(calculateXValue(currentDegree, 92, 100), calculateYValue(currentDegree, 92, 100), calculateXValue(currentDegree, 97, 100), calculateYValue(currentDegree, 97, 100), lcd.BLACK)
  # draw emphasis lines every 5 minutes on the clock face.
  # Every 5 Minute is 30 degree.
  for currentDegree in range(0, 331, 30):
    lcd.line(calculateXValue(currentDegree, 85, 100), calculateYValue(currentDegree, 85, 100), calculateXValue(currentDegree, 100, 100), calculateYValue(currentDegree, 100, 100), lcd.BLACK)
  label09.setText('9')
  label03.setText('3')
  label12.setText('12')
  label06.setText('6')
  # draw center of clock face
  circle0.setSize(4)

# Describe this function...
def updateDigitalClockFace():
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, year, month, day, hour, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  print("updateDigitalClockFace called...")
  currentTime = (str(addHeadingZeroToNumber(rtc.datetime()[4])) + str(((str(':') + str(addHeadingZeroToNumber(rtc.datetime()[5]))))))
  print("current Time: " + currentTime)
  label_weekday.setText(str((str('(') + str(((str(convertToLocale(rtc.datetime()[3])) + str(')')))))))
  label_clock.setText(str(currentTime))
  label_year.setText(str((rtc.datetime()[0]) + 2000))
  label_day.setText(str((str(addHeadingZeroToNumber(rtc.datetime()[2])) + str(((str('-') + str(addHeadingZeroToNumber(rtc.datetime()[1]))))))))

# Describe this function...
def adjustDayLightSaving(year, month, day, hour):
  global setActive, weekdayNumber, valueAsNumber, deg, len2, x, weekdayString, y, valueAsString, calculatedXValue, calculatedYValue, DEBUG, newTimeReceivedFromNTP, degHourHand, currentDegree, currentTime, fixedHour, enableDayLightSaving, TimeZone, degMinuteHand, dayLightSavingJson, WiFiSSID, WiFiPwd, currentStartEnd, dayLightSavingStartDay, dayLightSavingEndDay
  print("[adjustDayLightSaving]: called!")
  fixedHour = int(hour)
  if enableDayLightSaving:
    print("[adjustDayLightSaving]: Adjustment of day light saving time is enabled.")
    # This JSON holds all daylight saving dates from 2024 till 2038.
    # # Pattern:
    #   "24": {
    #     "start": 10,
    #     "end": 3
    #   },
    # #Where start is always in march (3) and end is always in October (10)
    dayLightSavingJson = json.loads('{"2024":{"start":31,"end":27},"2025":{"start":30,"end":26},"2026":{"start":29,"end":25},"2027":{"start":28,"end":31},"2028":{"start":26,"end":29},"2029":{"start":25,"end":28},"2030":{"start":31,"end":27},"2031":{"start":30,"end":26},"2032":{"start":28,"end":31},"2033":{"start":27,"end":30},"2034":{"start":26,"end":29},"2035":{"start":25,"end":28},"2036":{"start":30,"end":26},"2037":{"start":29,"end":25},"2038":{"start":28,"end":31}}')
    print("[adjustDayLightSaving]: JSON with daylight saving times loaded from String.")
    print(dayLightSavingJson)
    if month == 1 or month == 2 or month == 11 or month == 12:
      print("[adjustDayLightSaving]: Jan, Feb, Nov, Dez always is normal time. Keep time from NTP.")
      fixedHour = fixedHour + 0
    elif month == 4 or month == 5 or month == 6 or month == 7 or month == 8 or month == 9:
      print("[adjustDayLightSaving]: Apr, May, Jun, Jul, Aug, Sep always is summer time. Add +1 to Time from NTP")
      fixedHour = fixedHour + 1
    elif month == 3 or month == 10:
      print("[adjustDayLightSaving]: March and Oktober has dayLight saving depending on the day on the month")
      currentStartEnd = ''
      dayLightSavingStartDay = ''
      dayLightSavingEndDay = ''
      currentStartEnd = dayLightSavingJson[str(year)]
      print(currentStartEnd)
      dayLightSavingStartDay = int(currentStartEnd["start"])
      dayLightSavingEndDay = int(currentStartEnd["end"])
      # In Mrz and Oct day light saving time depends on day of the month.
      if int(day) == int(dayLightSavingStartDay) and int(month) == 3:
        print("[adjustDayLightSaving]: Day to change from winter/summer time detected. ")
        if int(hour) >= 2:
          print("[adjustDayLightSaving]: Beginning with 02:00 add +1 h to NTP time")
          fixedHour = fixedHour + 1
        else:
          print("[adjustDayLightSaving]: It's still winter time add +0 h to NTP time")
          fixedHour = fixedHour + 0
      elif int(day) == int(dayLightSavingEndDay) and int(month) == 10:
        print("[adjustDayLightSaving]: Day to change from summer/winter time detected.")
        if int(hour) >= 3:
          print("[adjustDayLightSaving]: Beginning with 03:00 add +0 h to NTP time")
          fixedHour = fixedHour + 0
        else:
          print("[adjustDayLightSaving]: It's still simmer time add +1 h to NTP time")
          fixedHour = fixedHour + 1
      elif int(day) >= int(dayLightSavingStartDay) and int(month) == 3 or int(day) < int(dayLightSavingEndDay) and int(month) == 10:
        print("[adjustDayLightSaving]: Daytime saving time detected. Add +1 h to NTP time.")
        fixedHour = fixedHour + 1
      else:
        print("[adjustDayLightSaving]: Normal time detected. Add +0 h to NTP time.")
        fixedHour = fixedHour + 0
  else:
    print("[adjustDayLightSaving]: adjustment of day light saving time was disabled.")
  return int(fixedHour)


def buttonEXT_wasPressed():
  global weekdayString, valueAsString, calculatedXValue, weekdayNumber, calculatedYValue, DEBUG, setActive, newTimeReceivedFromNTP, degHourHand, currentTime, fixedHour, enableDayLightSaving, valueAsNumber, TimeZone, x, y, degMinuteHand, hour, len2, currentDegree, dayLightSavingJson, WiFiSSID, WiFiPwd, deg, currentStartEnd, month, dayLightSavingStartDay, dayLightSavingEndDay, day
  print("EXT Button was pressed...")
  updateRTCwithDateTimeFromNTP()
  updateAndDrawClockFace()
  pass
btnEXT.wasPressed(buttonEXT_wasPressed)

@timerSch.event('timerRTC')
def ttimerRTC():
  global weekdayString, valueAsString, calculatedXValue, weekdayNumber, calculatedYValue, DEBUG, setActive, newTimeReceivedFromNTP, degHourHand, currentTime, fixedHour, enableDayLightSaving, valueAsNumber, TimeZone, x, y, degMinuteHand, hour, len2, currentDegree, dayLightSavingJson, WiFiSSID, WiFiPwd, deg, currentStartEnd, month, dayLightSavingStartDay, dayLightSavingEndDay, day
  print("updateRTC due to timer..")
  updateRTCwithDateTimeFromNTP()
  pass

@timerSch.event('timerUpdateClockFace')
def ttimerUpdateClockFace():
  global weekdayString, valueAsString, calculatedXValue, weekdayNumber, calculatedYValue, DEBUG, setActive, newTimeReceivedFromNTP, degHourHand, currentTime, fixedHour, enableDayLightSaving, valueAsNumber, TimeZone, x, y, degMinuteHand, hour, len2, currentDegree, dayLightSavingJson, WiFiSSID, WiFiPwd, deg, currentStartEnd, month, dayLightSavingStartDay, dayLightSavingEndDay, day
  print("updateClockFace due to timer..")
  updateAndDrawClockFace()
  pass


print("===============CLOCK WORK================")
print("$  Enable Debug on terminal:")
print("$  sudo apt-get install minicom")
print("$  sudo dmesg | grep tty")
print("$  sudo minicom -b 115200 -o -D /dev/ttyACM0")
print("===========================================")
DEBUG = True
enableDayLightSaving = True
# Set Timezone:
# UTC+1 = 1
# UTC-1 = -1
TimeZone = 1
if DEBUG:
  print("===========================================")
  print("Debung-Mode is enabled. WiFi Module is not shut shown." )
  print("===========================================")
else:
  print("===========================================")
  print("Debung-Mode is disabled. WiFi Module is shut shown, between NTP updates.")
  print("===========================================")
wlan = network.WLAN(network.STA_IF)
WiFiSSID = 'M5'
WiFiPwd = 'someSecretWiFiPassword'
# 3600000 ms = 1 h
timerSch.run('timerRTC', 3600000, 0x00)
timerSch.run('timerUpdateClockFace', 30000, 0x00)
updateRTCwithDateTimeFromNTP()
updateAndDrawClockFace()
# draw everthing
coreInkShow()
M5Led.off()
