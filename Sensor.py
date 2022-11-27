import board
import busio
import time
import adafruit_bmp280
import json
#spreadSheetLibs
import gspread
#import pandas as pd
import time
from gpiozero import MotionSensor
from gpiozero import LED
from oauth2client.service_account import ServiceAccountCredentials

#Sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
sensor.sea_level_pressure=1013.25

#Sensor infrarrojo
sensor_infrarrojo = MotionSensor(4)

#LED
led_verde = LED(14)
led_rojo = LED(15)

#SpreadSheet
scope_app =['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 
cred = ServiceAccountCredentials.from_json_keyfile_name('datos.json',scope_app) 
client = gspread.authorize(cred)
sheet = client.open('Data')
worksheet = sheet.worksheet('Datas')
worksheet2 = sheet.worksheet('Datas1')

id = int(worksheet.cell(2,11).value)
while True:
    #worksheet.update_cell(id+3,1,str(id))
    sensor_infrarrojo.wait_for_no_motion()
    temp = round(sensor.temperature, 2)
    press = round(sensor.pressure, 2)
    alt = round(sensor.altitude, 2)
    #print("Temperature: "+ str(temp) + "°C  "+"Pressure: "+str(press)+"   Altitude: " + str(alt))
    worksheet2.update_cell(id+1,1,str(temp))
    if(temp>27):
        led_rojo.on()
    else:
        led_verde.on()
    #worksheet.update_cell(id+3,4,str(alt))
    #worksheet.update_cell(id+3,5,str(press))
    
    #worksheet.update_cell(3,7,str(temp))
    #worksheet.update_cell(3,8,str(alt))
    #worksheet.update_cell(3,9,str(press))
    
    id+=1
    if(id==500):
        id=0
    worksheet.update_cell(2,11,str(id))
    time.sleep(2)
    led_rojo.off()
    led_verde.off()