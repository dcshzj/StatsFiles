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

import os
import sys
import settings

# Configuration to go into settings.py!
# Declare those globals first
accesskey = settings.accesskey
secretkey = settings.secretkey
collection = settings.collection
mediatype = settings.mediatype
path = settings.path
month = settings.month
year = settings.year

# Nothing to change below...
desc = "" # Item description
identifier = "" # Item URL
lastday = ""
monthname = ""
sizehint = "107374182400" # 100GB

def welcome():
	print "Welcome to the item creator script for the Wikimedia visitor statistics files!"

def bye(itemname):
	print "Item is created (called %s). Continue with the statsfiles.py file to upload the main files!" % (itemname)

def makemonthname():
	global lastday, month, monthname, year
	if (month == "01"):
		monthname = "January"
	elif (month == "02"):
		monthname = "February"
	elif (month == "03"):
		monthname = "March"
	elif (month == "04"):
		monthname = "April"
	elif (month == "05"):
		monthname = "May"
	elif (month == "06"):
		monthname = "June"
	elif (month == "07"):
		monthname = "July"
	elif (month == "08"):
		monthname = "August"
	elif (month == "09"):
		monthname = "September"
	elif (month == "10"):
		monthname = "October"
	elif (month == "11"):
		monthname = "November"
	elif (month == "12"):
		monthname = "December"
	else:
		print "ERROR: Month variable needs to be an integer! If the number is a single value, add a zero at the back please!"
		sys.exit() # Exit, there is nothing we need to do already zzz

def dldmd5sum():
	global month, year
	os.system("wget -c http://dumps.wikimedia.org/other/pagecounts-raw/%s/%s-%s/md5sums.txt" % (year, year, month))

def createitem():
	global month, monthname, year
	curl = ['curl', '--retry 20', '--location',
		'--header', "'x-amz-auto-make-bucket:1'",
		'--header', "'x-archive-meta01-collection:%s'" % (collection),
		'--header', "'x-archive-meta-mediatype:%s'" % (mediatype),
		'--header', "'x-archive-queue-derive:0'",
		'--header', "'x-archive-size-hint:%s'" % (sizehint),
		'--header', "'x-archive-meta-title:Wikimedia projects visitor statistics, raw hourly logfiles for %s %s (%s %s)'" % (monthname, year, monthname, year),
		'--header', "'x-archive-meta-description:%s'" % (desc),
		'--header', '"authorization: LOW %s:%s"' % (accesskey,secretkey),
		'--upload-file', "md5sums.txt http://s3.us.archive.org/%s/md5sums.txt" % (identifier),
		]
	os.system(' '.join(curl))

def generatestuff():
	global desc, identifier, month, monthname, year
	# Generate the identifier first
	identifier = "wikipedia_visitor_stats_%s%s" % (year, month)
	# Now generate the description
	tempdesc = ['Two log files (pagecounts, projectcounts) for each hour of',
			'%s %s.' % (monthname, year),
			'The timestamp is in the filename.',
			'The files were produced like this by Domas Mituzas, copied verbatim from his server',
			'and uploaded to the Internet Archive.',
			'For documentation see the oldest files from December 2007 or the new Wikimedia Foundation host.',
			]
	desc = ' '.join(tempdesc)

def process():
	global identifier
	welcome()
	makemonthname()
	dldmd5sum()
	generatestuff()
	createitem()
	bye(identifier)

if __name__ == "__main__":
	process()
