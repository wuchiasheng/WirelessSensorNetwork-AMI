"""
    Continuously read the serial port and process IO data received from a remote XBee.
    Depedency:1)https://pypi.python.org/pypi/XBee/2.1.0
    2)database.py
    """

#from xbee import XBee
from database import DBConnector
from databaseRemote import DBRemoteConnector
import serial
import re
import time
from datetime import datetime
import googledatastore as datastore
from googledatastore.helper import *
#Initialization
ser = serial.Serial('/dev/ttyS0', 38400)
#xbee = XBee(ser)
d = DBConnector()
dr = DBRemoteConnector()
datastore.set_options(dataset="gothic-standard-616")

#Continuously read/parse/store packets
while True:
	
	"""
        read raw data from xbee
        """
	dataStr = ''
	msgStr = ''
    
    #response = xbee.wait_read_frame()
	while(dataStr!='<'):
		response = ser.read()
		dataStr = str(response)
		msgStr = msgStr + dataStr
    #print dataStr
    
	print msgStr
    
	"""
        extract node id
        """
	m=re.search(r'NID:(\w+)',msgStr);
 	if(m):
		nid=m.group(1)
		print nid
        
		"""
            store various measurement result into databse
            """
        Results=re.findall(r'#(\w+):(\d+[.]?[\d]?[\d]?[\d]?)',msgStr)
		for result in Results:
			print result[0]	#quantity
			print result[1]	#value
			d.store(nid,80,result[0],result[1],result)
			dr.store(nid,80,result[0],result[1],result)
			
            
			#Google datastore integration
			req = datastore.CommitRequest()
			req.mode = datastore.CommitRequest.NON_TRANSACTIONAL
			sensor = req.mutation.insert_auto_id.add()
            #define entity path
			path = sensor.key.path_element.add()
            path.kind = 'sensorParser'
            # Add 3 entity properties:sensorName,sensorID,dateTime
            prop = sensor.property.add()
            prop.name = 'sensorID'
            prop.value.string_value = nid
            prop = sensor.property.add()
            prop.name = 'sensorName'
            prop.value.string_value = result[0]
			prop = sensor.property.add()
			prop.name = 'sensorValue'
			prop.value.string_value = result[1]
			prop = sensor.property.add()
			prop.name ='dateTime'
			prop.value.timestamp_microseconds_value =to_timestamp_usec(datetime.now())
			datastore.commit(req)
#Termination
ser.close()