# I have a csv which looks like this
    # Rankings,University,Overall,Teaching,Research,Environment,Research,Quality,Industry,International Outlook
    # 1,University of OxfordUnited Kingdom,98.5,96.6,100,99,98.7,97.5
    # 2,Stanford UniversityUnited States,98,99,97.8,99.6,100,87
    # 3,Massachusetts Institute of TechnologyUnited States,97.9,98.6,96.2,99.7,100,93.8

# I wish to seperate the country from university name, following program does that and writes the corrected data to a csv file

import re, csv, chardet, logging
from urllib import *
from urllib.request import *

logging.basicConfig(filename='projectLog.log', encoding='utf-8', level=logging.DEBUG)

# siplitter is a function which corrects the university and country name data part
# input for siplitter ['Stanford','UniversityUnited','States']
# output of siplitter ['Stanford University', 'United States'] 
def siplitter(a):
    for i,j in enumerate(a):
        x=re.findall("[A-Z][a-z]+",j)
        if len(x) > 1:
            uni = " ".join(a[:i])+" "+x[0]
            country= x[1]+" "+" ".join(a[i+1:])
            return [uni,country]

# urllib is a python module that is used to fetch pages from internet but in the following example it opens a local file
# following code uses urllibs pathname2url function to open a file on the disk
filepath=r"--path to csv file--"
fileurl=r"file:"+pathname2url(filepath)
rawfile=urlopen(fileurl, data=None, cafile=None, capath=None, cadefault=False, context=None).read()

# I use chardet module to detect the encoding of the file 
fileencoding=chardet.detect(rawfile)["encoding"]

# default mode for open() is - for reading
with open(filepath,encoding=fileencoding) as readfile:
    readcsv=csv.reader(readfile)
    next(readcsv)
    # newline="" to avoid extra blank line in the csv file
    with open(r"--path to new csv file--","w",newline='') as writefile:
        # use csveriter to read the csv
        writecsv=csv.writer(writefile)
        for row in readcsv:
            #adding try except here as often errors pop up during writing a csv file
            try:        
                listtowrite=row[0].split()+siplitter(row[1].split())+row[2:]
                writecsv.writerow(listtowrite)
            except:
                # logging.exception("") writes traceback to the log file
                logging.exception("")