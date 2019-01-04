#/usr/bin/python
#
# lib functions for remcom: remove commercials

import glob
import pickle
import psycopg2
from ConfigParser import ConfigParser



# ##################################################
# connect to *** odoo *** database

def connectDatabase():
	configFile = 'remcom.ini'
	configSection = 'database'

	parser = ConfigParser()
	parser.read(configFile)

	dbConfig = {}
	if parser.has_section(configSection):
		params = parser.items(configSection)
		for param in params:
			dbConfig[param[0]] = param[1]
	else:
		raise Exception('file {1}: Section {0} not found '.format(configSection, configFile))
		globals.logger.error('dblog.ini error: section ' + configSection + 'not found')

	# connect to odoo database
	conn = None
	try:
		logonstring = 'host=' + dbConfig['host'] + ' dbname=' + dbConfig['database'] + ' user=' + dbConfig['user'] + ' password=' + dbConfig['password']
		conn = psycopg2.connect(logonstring)
	except psycopg2.DatabaseError as e:
		print 'dblog.__init__():cannot connect to database ' + dbConfig['database'] + ' on ' + dbConfig['host']
		print e.pgerror
		globals.logger.error(
			'dblog.__init__():cannot connect to database ' + dbConfig['database'] + ' on ' + dbConfig['host'] + ' / ' + str(e.pgerror))
		exit(3)
	return conn


# ###############################################
# read hashes from database

def readHashes():

	conn = connectDatabase()
	cur = conn.cursor()
	cur.execute("select hash from hashes")
	hashlist = cur.fetchall()
	return hashlist

# ###############################################
# write hashes from database

def writeHashes(conn, item):
	cur = conn.cursor()

	statement = "insert into hashes (name, hash) values ("
	statement += "'" + item['name'] + "', "
	statement += "'" + item['hash'] + "')"
	statement += " on conflict (hash) do update set (name) = ("
	statement += "'" + item['name'] + "')"

	try:
		cur.execute(statement)
	except psycopg2.Error as e:
		print 'error in upsert location'
		print e.pgerror
		print 'ERROR upsert into table hashes, hash:' + item['hash'] + '   name: ' + item['names']
	finally:
		conn.commit()


# get all files in a directory
# use path + extenstion as arg, e.g. './dir/*.bmp'

def getFilesFromDir(name):
    return glob.glob(name)


def writeToPickle(l, filename):
    with open(filename, 'wb') as f:
        pickle.dump(l, f)

def readFromPickle(filename):
    with open(filename, 'rb') as f:
        l = pickle.load(f)
    return l
