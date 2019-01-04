#!/usr/bin/python
# This Python file uses the following encoding: utf-8
#
# test fftime

from fftime import *


if __name__ == '__main__':
	t = fftime()

	t.set(2, 0, 1)
	for i in range(0, 200):
		t.subtractminute()
		print t.string()


