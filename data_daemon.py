import Adafruit_BBIO.GPIO as GPIO
import time
import math
import requests
import os
import signal
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Adafruit_I2C import Adafruit_I2C
from bbio import *
from ctypes import c_short


bmp_addr = 0x77
i2c = Adafruit_I2C(bmp_addr)

GPIO.setup("P9_23",GPIO.OUT)             #Moisture Sensor Power

GPIO.setup("P8_7",GPIO.OUT)             #LED1
GPIO.setup("P8_8",GPIO.OUT)             #LED2
GPIO.setup("P8_9",GPIO.OUT)             #LED3
GPIO.setup("P8_10",GPIO.OUT)             #LED4
GPIO.setup("P8_11",GPIO.OUT)             #LED5
GPIO.setup("P8_12",GPIO.OUT)             #LED6
GPIO.setup("P8_15",GPIO.OUT)             #LED7
GPIO.setup("P8_16",GPIO.OUT)             #LED8

#Turns on 'num' LEDs. If num>8 all LEDs are lit.
def leds_on(num):
    if num==0:
        GPIO.output("P8_7",GPIO.LOW)             #LED1
        GPIO.output("P8_8",GPIO.LOW)             #LED2
        GPIO.output("P8_9",GPIO.LOW)             #LED3
        GPIO.output("P8_10",GPIO.LOW)             #LED4
        GPIO.output("P8_11",GPIO.LOW)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==1:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.LOW)             #LED2
        GPIO.output("P8_9",GPIO.LOW)             #LED3
        GPIO.output("P8_10",GPIO.LOW)             #LED4
        GPIO.output("P8_11",GPIO.LOW)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==2:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.LOW)             #LED3
        GPIO.output("P8_10",GPIO.LOW)             #LED4
        GPIO.output("P8_11",GPIO.LOW)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==3:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.LOW)             #LED4
        GPIO.output("P8_11",GPIO.LOW)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==4:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.HIGH)             #LED4
        GPIO.output("P8_11",GPIO.LOW)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==5:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.HIGH)             #LED4
        GPIO.output("P8_11",GPIO.HIGH)             #LED5
        GPIO.output("P8_12",GPIO.LOW)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==6:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.HIGH)             #LED4
        GPIO.output("P8_11",GPIO.HIGH)             #LED5
        GPIO.output("P8_12",GPIO.HIGH)             #LED6
        GPIO.output("P8_15",GPIO.LOW)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    elif num==7:
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.HIGH)             #LED4
        GPIO.output("P8_11",GPIO.HIGH)             #LED5
        GPIO.output("P8_12",GPIO.HIGH)             #LED6
        GPIO.output("P8_15",GPIO.HIGH)             #LED7
        GPIO.output("P8_16",GPIO.LOW)             #LED8
    else:       #num>=8
        GPIO.output("P8_7",GPIO.HIGH)             #LED1
        GPIO.output("P8_8",GPIO.HIGH)             #LED2
        GPIO.output("P8_9",GPIO.HIGH)             #LED3
        GPIO.output("P8_10",GPIO.HIGH)             #LED4
        GPIO.output("P8_11",GPIO.HIGH)             #LED5
        GPIO.output("P8_12",GPIO.HIGH)             #LED6
        GPIO.output("P8_15",GPIO.HIGH)             #LED7
        GPIO.output("P8_16",GPIO.HIGH)             #LED8

#Read from a byte of data from 'channel' on MCP008 and return value
def analog_read(channel):
  r = SPI0.transfer([1, (8 + channel) <<4, 0])
  adc_out = ((r[1]&3) <<8) + r[2]
  return adc_out

#Read from LDR to determine whether Night or Day
def get_night_day():
  reading = analog_read(7)
  voltage = reading*3.3/1024            #scale to 3.3V to determine acutal voltage
  print "LDR Sensor"
  print("Reading=%d\tVoltage=%f" % (reading, voltage))
  return ("Night" if reading<50 else "Day")
  
def get_soil_mos():
  GPIO.output("P9_23", GPIO.HIGH)     #Power up sensor
  time.sleep(0.005)
  reading = analog_read(6)            #take reading
  GPIO.output("P9_23", GPIO.LOW)      #power down sensor
  voltage = reading*3.3/1024            #scale to 3.3V to determine acutal voltage
  print "Soil Mos. Sensor"
  print("Reading=%d\tVoltage=%f" % (reading, voltage))
  mos_norm = (reading-6)*1000/(900-6)           #normalize [6, 900] to [0, 1000]
  num_leds = abs(int(mos_norm*8/1000))          #normalize to 8 (truncate decimal) and turn on LEDs
  leds_on(num_leds)           
  return mos_norm

#gets pressure and temperature from BMP180
def get_data_bmp():
  params = i2c.readList(0xAA, 22)       #read 12 coefficients from EEPROM

  AC1 = c_short((params[0] <<8) + params[1]).value
  AC2 = c_short((params[2] <<8) + params[3]).value
  AC3 = c_short((params[4] <<8) + params[5]).value
  AC4 = (params[6] <<8) + params[7]
  AC5 = (params[8] <<8) + params[9]
  AC6 = (params[10] <<8) + params[11]
  B1 = c_short((params[12] <<8) + params[13]).value
  B2 = c_short((params[14] <<8) + params[15]).value
  MB = c_short((params[16] <<8) + params[17]).value
  MC = c_short((params[18] <<8) + params[19]).value
  MD = c_short((params[20] <<8) + params[21]).value
  
  
  #start conversion and read temperature
  i2c.write8(0xF4, 0x2E)        
  time.sleep(0.01)                  #10 ms wait time for conversion
  msb = i2c.readU8(0xF6)
  lsb = i2c.readU8(0xF7)
  ut = (msb <<8) + lsb              #uncompensated temperature
  
  #start conversion and read pressure
  oss = 3          #over_sampling setting [0-3], 3 = 8 samples
  i2c.write8(0xF4, 0x34+(oss<<6))        
  time.sleep(0.05)                  #50 ms wait time for 8 samples
  msb = i2c.readU8(0xF6)
  lsb = i2c.readU8(0xF7)
  xlsb = i2c.readU8(0xF8)
  up = ((msb<<16)+(lsb<<8)+(xlsb)) >> (8-oss)   #uncompensated pressure
  
  #True Temperature
  X1 = (ut - AC6)*AC5/(2**15)
  X2 = (MC*(2**11))/(X1+MD)
  B5 = X1 + X2
  temp = (B5+8)/(2**4)
  
  #True Pressure
  B6 = B5 - 4000
  X1 = (B2*(B6*B6 >>12)) >>11
  X2 = (AC2*B6) >>11
  X3 = X1 + X2
  B3 = (((AC1*4+X3)<<oss)+2)/4
  X1 = (AC3*B6) >>13
  X2 = (B1*((B6*B6)>>12)) >>16
  X3 = ((X1+X2)+2) >>2
  B4 = (AC4*(X3+32768)) >>15
  B7 = (up-B3)*(50000>>oss)
  if (B7< 0x80000000):
      p = (B7*2)/B4
  else:
      p = (B7/B4)*2
  X1 = (p >>8)*(p >>8)
  X1 = (X1*3038) >>16
  X2 = (-7357*p) >>16
  pres = p+((X1+X2+3791)>>4)
  
  return (temp/10.0, pres)     #temp = C/ pres = Pa


#uploads file to gdrive
def upload_file(filename):
    gauth = GoogleAuth()                #authenticates application from 'client_secrets.json'
    gauth.LoadCredentialsFile("/var/lib/cloud9/mycreds.txt")    #Load credentials of gdrive user to uplaod files

    if gauth.credentials is None:           #if file is empty or credentials not valid
        gauth.CommandLineAuth()             #For the first time, key has to be entered manually
                                            #But should never reach here on crontab job (signal will terminate application after 20s),
    elif gauth.access_token_expired:            #if credentials expired, then refresh them
        gauth.Refresh()
    else:                                   #if stored credentials are good, then authenticate application user
        gauth.Authorize()                       
        
    gauth.SaveCredentialsFile("/var/lib/cloud9/mycreds.txt")        #save new credentials
    
    drive = GoogleDrive(gauth)
    
    file2 = drive.CreateFile()              #create file to upload
    file2.SetContentFile("/var/lib/cloud9/photos/" + str(filename) + ".jpg")        #write to file
    file2['title'] = str(filename) + ".jpg"                                   #file name
    file2.Upload()                                                              #upload file to gdrive
    print 'Created file %s on Google Drive' % (file2['title'])

    f = open('/var/lib/cloud9/photos/successful_uploads.txt', 'a')              #log if file uploaded successfully. if stuck on credentials, signal termiantes app and nothing is written.
    f.write(filename+".jpg"+"\n")
    f.close()

#retrive temperature and pressure
temp, pres = get_data_bmp()
SPI0.begin()
day_night = get_night_day()
mos = get_soil_mos()
SPI0.end()

os.system('echo "nameserver 8.8.8.8" >> /etc/resolv.conf')          #set DNS server
data = {'private_key':'xz5NWqy7p9FvX80yxBmz','bbbname':'RaghuParth_BBB', 'moisture':str(mos), 'night_or_day':str(day_night), 'pressure':str(pres), 'temp':str(temp)}
print data

r = requests.get('http://data.sparkfun.com/input/9J0nlOZ891hR4Mm1lNyp', params=data)      #send GET request to Sparkfun

print "TAKING PHOTO"
# Take Photo
time_stmp = time.time()
print "Time: ", str(int(time_stmp))
cmd_str = "fswebcam -r 640x480 /var/lib/cloud9/photos/" + str(int(time_stmp)) + ".jpg"
os.system(cmd_str)

#store data internally
f = open('/var/lib/cloud9/photos/data_log.txt', 'a')
f_str = str(int(time_stmp)) + " " + str(mos) + " " + day_night + " " + str(pres) + " " + str(temp) + "\n"
f.write(f_str)
f.close()

#upload file gdrive
signal.alarm(20)              #20 sec timer incase file upload fails
upload_file(str(int(time_stmp)))      #uplaod file with filename as current time (unix seconds)
print "EXITING"

print r.content       #print whether HTTP GET request was successful (1 Success)
