import pandas as pd
import os
import glob

# getting csv files from the folder MyProject
from fileinput import filename
path = os.getcwd()

# read all the files with extension .csv
filenames = glob.glob(path + "\*.txt")

# for loop to iterate all txt files
for file in filenames:
   # reading csv files
   d = pd.read_csv(file, sep=';')
   file_name = file.rsplit(' ', 1)[1]
   file_name = file_name.rsplit('.', 1)[0]
   d.to_excel(file_name + ".xlsx", index = False)  