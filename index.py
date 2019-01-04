# /usr/bin/python
#
# remcom: remove commercials
#
# index.py: create a list of all images from commercials and store them in database
#
# call python index.py filename.mp4 'commercials name'  e.g.
# python index.py giro2018-1.mp4 'Giro 2018'

import os, sys, shutil
from ConfigParser import ConfigParser

from PIL import Image

from dhash import *
from remcomlib import *


# create list of 8x8 hashes and write them to disk

def createIndex(imagepath):
	hashlist = []

	images = getFilesFromDir(imagepath)
	for f in images:
		image = Image.open(f)
		row, col = dhash_row_col(image)
		hash = format_hex(row, col)
		item = [f, hash]
		hashlist.append(item)
	return hashlist


if __name__ == '__main__':

	if len(sys.argv) != 3:
		print "index.py videofile 'name'"
		exit(1)

	# read ini file
	configFile = 'remcom.ini'
	configSection = 'remcom.index'
	parser = ConfigParser()
	parser.read(configFile)
	inifile = {}
	if parser.has_section(configSection):
		params = parser.items(configSection)
		for param in params:
			inifile[param[0]] = param[1]
	else:
		raise Exception('file {1}: Section {0} not found '.format(configSection, configFile))

	# create tmp dir
	try:
		if not os.path.exists(inifile['tmp']):
			os.makedirs(inifile['tmp'])
	except OSError:
		print ('Error: Creating directory. ' + inifile['tmp'])
		exit(2)
	print 'created tmp dir ' + inifile['tmp']

	# extract all images from video file to tmp directory
	print ' now extracting images . . .'
	command = 'ffmpeg -i ' + sys.argv[1] + ' ' + inifile['tmp'] + '/img%05d.jpg -hide_banner'
	os.system(command)

	hashlist = createIndex(inifile['tmp'] + '/*')
	writeToPickle(hashlist, inifile['pickle'])

	# remove tmp dir
	try:
		shutil.rmtree(inifile['tmp'])
	except OSError as e:
		print ("Error: %s - %s." % (e.filename, e.strerror))
	print 'finished !'
