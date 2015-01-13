# CAB010_CO_gov_CSV_scraper.py 

# -*- coding: utf-8 -*-

import os
import time
import urllib
import glob
import csv
import shutil
from bs4 import BeautifulSoup

# Set up variables
entity = "CAB010_CO_gov"
url = "https://www.gov.uk/government/publications/cabinet-office-spend-data"
downloaded = '/Users/ianmakgill/Dropbox (Ticon)/_File_processing/New_System/1_Downloaded/'+entity
renamed = '/Users/ianmakgill/Dropbox (Ticon)/_File_processing/New_System/2_Renamed_Files/'+entity
today = time.strftime("%Y-%m-%d")

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'Jan': '01', 'Feb': '02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09','Oct':'10','Nov':'11','Dec':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string


def move_amended_files():
	"move and rename any amended files (_out) to the right dir"
	source = os.listdir(downloaded)
	for files in source:
		if files.startswith('out_'):
			newName = files.replace('out_','')
			newPath = renamed+'/'+newName
			shutil.move(files,newPath)
	return


def write_new_file( fileName ):
# open the file and then add the extra columns
	with open(fileName, 'rb') as inf, open("out_"+fileName, 'wb') as outf:
		csvreader = csv.DictReader(inf)

		fieldnames = ['url_source','downloaded_at'] + csvreader.fieldnames  # add column names to beginning
		csvwriter = csv.DictWriter(outf, fieldnames)
		csvwriter.writeheader()
		for node, row in enumerate(csvreader, 1):
			csvwriter.writerow(dict(row, url_source=csvUrl, downloaded_at=today))
	return


# change dir
os.chdir(downloaded)
# get list of csv files in the directory
fileList = glob.glob("*.csv")

# pull down the content from the webpage
html = urllib.urlopen(url)
soup = BeautifulSoup(html)


# find all entries with the required class
blocks = soup.findAll('div', {'class':'attachment-details'})

for block in blocks:

	link = block.a['href']
	title = block.h2.contents[0]

	# add the right prefix to the url
	csvUrl = link.replace("/preview","")
	csvUrl = csvUrl.replace("/government","http://www.gov.uk/government")
	
	# create the right strings for the new filename
	csvYr = title.split(' ')[-1]
	csvMth = title.split(' ')[-2][:3]	

	csvMth = convert_mth_strings(csvMth);

	fileName = entity + "_" + csvYr + "_" + csvMth + ".csv"

	if fileName in fileList:
		print "already got file "+ fileName
	else:
		# download the file
		urllib.urlretrieve(csvUrl, os.path.basename(fileName))
		write_new_file(fileName);
		
	
	move_amended_files();

	
		
