import pandas as pd
import os
import glob
import numpy as np
import re

## For each text file in folder:
## 1) Create an excel extract
## 2) compare all matrix values and return:
##    a) occurrences of values (number of times a correlation was present)
##    b) Z-Score from correlation coefficient
##    c) Updated Correlation coefficient from an averaged z-score
# getting csv files from the folder MyProject
path = os.getcwd()

# read all the files with extension .csv
filenames = glob.glob(path + "\*.txt")
newpath = path+'/Extract'
if not os.path.exists(newpath):
   os.makedirs(newpath)

d_list = []
z_list = []
# for loop to iterate all txt files
# save copy for edit
for file in filenames:
   # reading csv files
   d = pd.read_csv(file, sep=';')
   file_name = file.rsplit(' ', 1)[1]
   file_name = file_name.rsplit('.', 1)[0]   
   #d.to_excel(newpath+"\\"+file_name + ".xlsx", index = False)  
   
   #z-score
   d_indexed = d.set_index('Matrix')
   
   ##(1/2)log( (1+r)/(1-r))
   numeric_cols = [col for col in d_indexed if d_indexed[col].dtype.kind != 'O']
   d_z_score = (1+d_indexed[numeric_cols]) / (1-d_indexed[numeric_cols])
   d_z_score = np.log10(d_calc) / 2
   d_z_score.reset_index(drop=False, inplace=True)

   #Export
   # create a excel writer object
   with pd.ExcelWriter(newpath+"\\"+file_name + ".xlsx") as writer:
      d.to_excel(writer, sheet_name="Extract", index=False)
      d_z_score.to_excel(writer, sheet_name="Z Scores", index=False)

   d_list.append(d)
   z_list.append(d_z_score)

df_final=pd.concat(d_list)
z_score=pd.concat(z_list)

#average Z_score
average_z_score = z_score.groupby('Matrix').mean()
#count of occurences
n_matrix = df_final.groupby('Matrix').count()

#export 
#file name
updated_file_name = file_name.split('_', 1)[-1]
updated_file_name = updated_file_name.split("_")[0]

nextpath = path+'/Calculated'
if not os.path.exists(nextpath):
   os.makedirs(nextpath)
# create a excel writer object
with pd.ExcelWriter(nextpath+"\\"+updated_file_name + ".xlsx") as writer:
   average_z_score.to_excel(writer, sheet_name="Average Z", index=True)
   n_matrix.to_excel(writer, sheet_name="Samples", index=True)