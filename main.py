"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

from xbee import XBee
from database import DBConnector
import serial
import re

#Initialization
ser = serial.Serial('/dev/ttyUSB1', 38400)#/dev/ could change,so verify in /dev
xbee = XBee(ser)
d = DBConnector()

#Continuously read/parse/store packets
while True:
    response = xbee.wait_read_frame()
	dataStr = str(response)
	print dataStr
	s2Results=re.findall(r'(<>)(S2) (\w+:)(\w+) (\w+:)(\w+) (\w+):(\w+.\w+) (\w+:)(\w+.\w+)',dataStr)#Extract data from S2 format only
    	for result in s2Results:
		print result[0] #<>
		print result[1]	#S2
		print result[2]	#MAC
		print result[3]	#val
		print result[4]	#ID
		print result[5]	#val
		print result[6]	#Temp
		print result[7] #val
        d.store(result[5],80,result[6],result[7],result)#Store temperature data in MeshliumDB
ser.close()
