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

# Configuration
path = "." # Path to temporarily store the stats files

# Nothing to change below
day = ""
identifier = ""
lastday = ""
month = int(sys.argv[1])
monthname = ""
year = int(sys.argv[2])
filename = ""
count = 0
# Can't help but make it this hackish...
hours = {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'}

def welcome():
	print "Welcome to the visitor statistics files archiving script!"

def bye():
	print "All done, good bye!"

def makelastday():
	global lastday, month, monthname, year
	if (month == 1):
		lastday = "32"
	elif (month == 2):
		# Leap years, support for the next 3 leap years only
		if (year == "2012"):
			lastday = "30"
		elif (year == "2016"):
			lastday = "30"
		elif (year == "2020"):
			lastday = "30"
		else:
			lastday = "29"
	elif (month == 3):
		lastday = "32"
	elif (month == 4):
		lastday = "31"
	elif (month == 5):
		lastday = "32"
	elif (month == 6):
		lastday = "31"
	elif (month == 7):
		lastday = "32"
	elif (month == 8):
		lastday = "32"
	elif (month == 9):
		lastday = "31"
	elif (month == 10):
		lastday = "32"
	elif (month == 11):
		lastday = "31"
	elif (month == 12):
		lastday = "32"
	else:
		print "ERROR: Month variable needs to be an integer! If the number is a single value, add a zero at the back please!"
		sys.exit() # Exit, there is nothing we need to do already zzz

def findidentifier():
	global identifier, month, year
	identifier = "wikipedia_visitor_stats_%s%s" % (year, month)

def generateFilenamelessthanten(syear, smonth, sday, shour):
	global filename
	if (smonth < 10):
		if (shour < 10):
			if (sday < 10):
				filename = "pagecounts-%d0%d0%d-0%d0000.gz" % (syear, smonth, sday, shour)
			else:
				filename = "pagecounts-%d0%d%d-0%d0000.gz" % (syear, smonth, sday, shour)
		else:
			if (sday < 10):
				filename = "pagecounts-%d0%d0%d-%d0000.gz" % (syear, smonth, sday, shour)
			else:
				filename = "pagecounts-%d0%d%d-%d0000.gz" % (syear, smonth, sday, shour)
	else:
		if (shour < 10):
			if (sday < 10):
				filename = "pagecounts-%d%d0%d-0%d0000.gz" % (syear, smonth, sday, shour)
			else:
				filename = "pagecounts-%d%d%d-0%d0000.gz" % (syear, smonth, sday, shour)
		else:
			if (sday < 10):
				filename = "pagecounts-%d%d0%d-%d0000.gz" % (syear, smonth, sday, shour)
			else:
				filename = "pagecounts-%d%d%d-%d0000.gz" % (syear, smonth, sday, shour)

def dldfilesoctnovdec():
	global day, hours, lastday, month, path, year, filename, count
	os.chdir(path)
	day = 01 # Lets start off with the first day of the month
	if (day < 10):
		if (count == 0):
			generateFilenamelessthanten(year, month, day, hour)
			print filename
			os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
			if (os.path.exists(filename)):
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0000" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			else:
				filename = "pagecounts-%s%s%s-%s0001.gz" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0001" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			day += 1
			count += 1
		else:
			for hour in hours:
				if (day == 01 and hour == 00):
					continue
				else:
					generateFilename(year, month, day, hour)
					print filename
					os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
					if (os.path.exists(filename)):
						uploadfile(filename)
						brotherfile = "projectcounts-%s%s%s-%s0000" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
						uploadfile(brotherfile)
					else:
						filename = "pagecounts-%s%s%s-%s0001.gz" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
						uploadfile(filename)
						brotherfile = "projectcounts-%s%s%s-%s0001" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
						uploadfile(brotherfile)
					day += 1
			count = 0

def dldfilesrest():
	global day, hours, lastday, month, path, year, filename, count
	os.chdir(path)
	day = 01 # Lets start off with the first day of the month
	if (day < 10):
		if (count == 0):
			hour = 00
			generateFilenamelessthanten(year, month, day, hour)
			print filename
			os.system('wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s') % (year, year, month, filename)
			if (os.path.exists(filename)):
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0000" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			else:
				filename = "pagecounts-%s%s%s-%s0001.gz" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
				uploadfile(filename)
				brotherfile = "projectcounts-%s%s%s-%s0001" % (year, month, day, hour)
				os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
				uploadfile(brotherfile)
			day += 1
			count += 1
		else:
			for hour in hours:
				if (day == 01 and hour == 00):
					continue
				else:
					generateFilename(year, month, day, hour)
					print filename
					os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
					if (os.path.exists(filename)):
						uploadfile(filename)
						brotherfile = "projectcounts-%s%s%s-%s0000" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
						uploadfile(brotherfile)
					else:
						filename = "pagecounts-%s%s%s-%s0001.gz" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, filename)
						uploadfile(filename)
						brotherfile = "projectcounts-%s%s%s-%s0001" % (year, month, day, hour)
						os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%d/%d-%d/%s") % (year, year, month, brotherfile)
						uploadfile(brotherfile)
					day += 1
			count = 0

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

def shuffler():
	global month
	if (month < 10):
		dldfilesrest()
	else:
		dldfilesoctnovdec()

def process():
	welcome()
	findidentifier()
	makelastday()
	shuffler()
	bye()

if __name__ == "__main__":
	process()
