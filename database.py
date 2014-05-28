"""
 Store data in MeshliumDB database created in local host
"""
import MySQLdb
from ConfigParser import SafeConfigParser

class DBConnector:
	def store(self,id,frameType,sensorType,sensorVal,raw):
		print 'Trying to connect with MySQL'
		parser = SafeConfigParser()
		parser.read('dbconfig.ini')
		
		try:
			conn=MySQLdb.connect(host=parser.get('MeshliumDB','host'),user="root",passwd=parser.get('MeshliumDB','passwd'),db="MeshliumDB")
			x=conn.cursor()
			print 'Connected to MySQL'
			
			try:
				x.execute("INSERT INTO sensorParser values(default,'" +id+ "','" +id+ "',default,'" +sensorType+ "','" +sensorVal+ "',now(),1,'raw')")
				conn.commit()
				conn.close()
			except MySQLdb.Error,e:
				print "MYSQL Error"
		except MySQLdb.Error, e:
			print "MYSQL Error"
				
