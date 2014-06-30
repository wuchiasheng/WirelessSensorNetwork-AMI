"""
    Continuously read the serial port and process IO data received from a remote XBee.
    Google datastore integration
    """

#from xbee import XBee
from database import DBConnector
from databaseRemote import DBRemoteConnector
import serial
import re
import time
import googledatastore as datastore

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
            """
            Local & Remote MySQL insertion
            """
            print result[0]	#quantity
			print result[1]	#value
			d.store(nid,80,result[0],result[1],result)
			dr.store(nid,80,result[0],result[1],result)
			
            """
            Google datastore insertion
            """
            # Create a RPC request to begin a new transaction.
            req = datastore.BeginTransactionRequest()
   		 	# Execute the RPC synchronously.
            resp = datastore.begin_transaction(req)
            # Get the transaction handle from the response.
            tx = resp.transaction
            # Create a RPC request to get entities by key.
            req = datastore.LookupRequest()
            # Create a new entity key.
            key = datastore.Key()
            # Set the entity key with only one `path_element`: no parent.
            path = key.path_element.add()
            path.kind = 'sensorParser'
			path.name = time.strftime("%d%m%Y%H%M%S")
            # Add one key to the lookup request.
            req.key.extend([key])
            # Set the transaction, so we get a consistent snapshot of the
            # entity at the time the transaction started.
            req.read_options.transaction = tx
            # Execute the RPC and get the response.
            resp = datastore.lookup(req)
            # Create a RPC request to commit the transaction.
   			req = datastore.CommitRequest()
   			# Set the transaction to commit.
            req.transaction = tx
			entity = req.mutation.insert.add()
            # Copy the entity key.
            entity.key.CopyFrom(key)
            # Add two entity properties:
            # - a utf-8 string: `question`
            prop = entity.property.add()
            prop.name = 'sensorID'
            prop.value.string_value = nid
            # - a 64bit integer: `answer`
            prop = entity.property.add()
            prop.name = 'sensorName'
            prop.value.string_value = result[0]
			prop = entity.property.add()
			prop.name = 'sensorValue'
			prop.value.string_value = result[1]
            # Execute the Commit RPC synchronously and ignore the response:
            # Apply the insert mutation if the entity was not found and close
            # the transaction.
            datastore.commit(req)

#Termination
ser.close()