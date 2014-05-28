import MySQLdb
from ConfigParser import SafeConfigParser
from encrypt import encrypt_RSA
from decrypt import decrypt_RSA

class DBConnector:
	def store(self,id,frameType,sensorType,sensorVal,raw):
		print 'Trying to connect with MySQL'
		parser = SafeConfigParser()
		parser.read('dbconfig.ini')
		
		try:
			encryptedPasswd = parser.get('MeshliumDB','passwd')
			decryptedPasswd= decrypt_RSA("xx",encryptedPasswd)
			conn=MySQLdb.connect(host=parser.get('MeshliumDB','host'),user="root",passwd=decryptedPasswd,db="MeshliumDB")
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
				
