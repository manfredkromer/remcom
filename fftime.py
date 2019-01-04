#!/usr/bin/python
# This Python file uses the following encoding: utf-8
#
# define a ffpmeg time object

class fftime():
	def __init__(self):
		seconds = 0
		minutes = 0
		hours = 0

	def reset(self):
		seconds = 0
		minutes = 0
		hours = 0

	def set(self, hours = 0, minutes = 0, seconds = 0):
		self.hours = hours
		self.minutes = minutes
		self.seconds = seconds
		self.checkOverflow()

	# increment by one second
	def addsecond(self, s = 1):
		self.seconds = self.seconds + s
		self.checkOverflow()

	# decrement by one second
	def subtractsecond(self, s = 1):
		self.seconds = self.seconds - s
		self.checkOverflow()

	# increment by one minute
	def addminute(self, s=1):
		self.minutes = self.minutes + s
		self.checkOverflow()

	# decrement by one minute
	def subtractminute(self, s=1):
		self.minutes = self.minutes - s
		self.checkOverflow()

	def string(self):
		s = str(self.hours) + ':' + str(self.minutes) + ':' + str(self.seconds)
		return s


	def printfftime(self):
		print 'fftime: ' + str(self.hours) + ':' + str(self.minutes) + ':' + str(self.seconds)

	def checkOverflow(self):
		if self.seconds >= 60:
			self.seconds = 0
			self.minutes = self.minutes + 1
		if self.minutes >= 60:
			self.minutes = 0
			self.hours = self.hours + 1
		if self.hours >= 24:
			raise Exception('fftime overflow !')

		if self.seconds < 0:
			self.seconds = 59
			self.minutes = self.minutes - 1
		if self.minutes < 0:
			self.minutes = 59
			self.hours = self.hours - 1
		if self.hours < 0:
			raise Exception('fftime underflow !')