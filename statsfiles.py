#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Hydriz
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import boto
from boto.s3.key import Key
import os
import sys

# Nothing to change below
day = ""
identifier = ""
lastday = ""
month = sys.argv[1]
monthname = ""
year = sys.argv[2]
# Can't help but make it this hackish...
hours = {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'}

def welcome():
	print "Welcome to the visitor statistics files archiving script!"

def bye():
	print "All done, good bye!"

def makelastday():
	global lastday, month, monthname, year
	if (month == "01"):
		lastday = "31"
	elif (month == "02"):
		# Leap years, support for the next 3 leap years only
		if (year == "2012"):
			lastday = "29"
		elif (year == "2016"):
			lastday = "29"
		elif (year == "2020"):
			lastday = "29"
		else:
			lastday = "28"
	elif (month == "03"):
		lastday = "31"
	elif (month == "04"):
		lastday = "30"
	elif (month == "05"):
		lastday = "31"
	elif (month == "06"):
		lastday = "30"
	elif (month == "07"):
		lastday = "31"
	elif (month == "08"):
		lastday = "31"
	elif (month == "09"):
		lastday = "30"
	elif (month == "10"):
		lastday = "31"
	elif (month == "11"):
		lastday = "30"
	elif (month == "12"):
		lastday = "31"
	else:
		print "ERROR: Month variable needs to be an integer! If the number is a single value, add a zero at the back please!"
		sys.exit() # Exit, there is nothing we need to do already zzz

def findidentifier():
	global identifier, month, year
	identifier = "wikipedia_visitor_stats_%s%s" % (year, month)

def dldfiles():
	global day, hours, lastday, month, path, year
	os.chdir(path)
	madeupday = lastday + 1
	day = 1 # Lets start off with the first day of the month
	hour = 01
	while (day < madeupday):
		for hour in hours:
			filename = "pagecounts-%s%s%s-%s0000.gz" % (year, month, day, hour)
			os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%s/%s-%s/%s") % (year, year, month, filename)
			if (os.path.exists(filename)):
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0000" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%s/%s-%s/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			else:
				filename = "pagecounts-%s%s%s-%s0001.gz" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%s/%s-%s/%s") % (year, year, month, filename)
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0001" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%s/%s-%s/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			day += 1

def uploadfile(thefile):
	global identifier
	conn = boto.connect_s3(host='s3.us.archive.org', is_secure=False)
	bucket = conn.get_bucket(identifier) # Item should have been created by createitem.py
	if not bucket:
		sys.exit("ERROR: You need to run createitem.py first before running this script!")
	k = Key(bucket)
	k.key = thefile
	headers = {}
	headers['x-archive-queue-derive'] = '0'
	k.set_contents_from_filename(thefile,headers=headers,num_cb=10)

def process():
	welcome()
	findidentifier()
	makelastday()
	dldfiles()
	bye()

if __name__ == "__main__":
	process()
