# A program to sort photos with creation date and to put them into folders named by years and subfolders within the year's folder named by months respectively

import os, shutil, calendar, logging
from datetime import datetime

# logging config
logging.basicConfig(filename='projectLog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# root directory of the folders which contains the photos
rootdirectory = r"--some_path--"
# path where you want year/month folders to be
monthsfolderdir = r"--some_path--" 

formats = [".jpg",".jpeg",".bmp",".png"]

# Walk through the directory and its subdirectories
for foldername, subfolders, filenames in os.walk(rootdirectory):    
    # List the filenames in the current folder
    for filename in filenames:
        if [i for i in formats if i in filename]:
            photopath = os.path.join(foldername, filename)    
            # get EXIF data with a creation date.
            creationdate = datetime.fromtimestamp(os.path.getctime(photopath))
            # Create a year and month folder
            year = creationdate.strftime("%Y")
            month = calendar.month_name[int(creationdate.strftime("%m"))]
            yearfolderpath = os.path.join(monthsfolderdir, year)
            os.makedirs(yearfolderpath, exist_ok=True)
            monthfolderpath = os.path.join(yearfolderpath, month)
            os.makedirs(monthfolderpath, exist_ok=True)
            check=os.path.join(monthfolderpath,filename)
            # check if file exists at the destination
            if not os.path.exists(check):
                # Move the photo to the month folder
                shutil.move(photopath, monthfolderpath)
                print(f"Moved {photopath} to {monthfolderpath}")
            else:
                logging.info(f"File {photopath} exists in the destination folder.")
