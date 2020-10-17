import os
import xarray as xr
import pandas as pd
import csv
from csv import writer
from csv import reader
from glob import glob
import numpy as np
import sys

#
# if len(sys.argv) < 1:
#     print('usage: DBquery.py inputPath/ outputPath/')
#     exit(1)

# outPath = sys.argv[2]
# inPath = sys.argv[1]
r = 20
item = '/home/sli/Downloads/csv/wrf5_d03_20200801Z0300.nc.nc4.csv'
# for item in os.listdir(inPath):
#     if item.endswith(".csv"):
df = pd.read_csv(item)
tmp = df.loc[df['light'] == 1]
# x = df[['X']].to_numpy()
# y = df[['Y']].to_numpy()
# cx = tmp['X'].to_numpy()
# cy = tmp['Y'].to_numpy()


for i in range(len(tmp)):
    cx = tmp.values[i][38]
    cy = tmp.values[i][39]
    if i == 0:
        row = df[(df.X - cx) ** 2 + (df.Y - cy) ** 2 < r ** 2]
    row = row.append(df[(df.X - cx) ** 2 + (df.Y - cy) ** 2 < r ** 2], ignore_index=True)

print(row)
row.to_csv('/home/sli/Downloads/circle.csv')

# Nump = df[['X', 'Y']].to_numpy()
# coords = tmp[['X', 'Y']].to_numpy()
#
# # for item in coords:
# #     for elem in Nump:
#
# df1 = np.where(((x[:]-cx[:])**2 + (y[:]-cy[:])**2) < r**2)
#
# for i in range(len(df1[1])):
#     print(str(df1[0][i]) + '\t' + str(df1[1][i]))

# print(df1[0][:])
# print('\t')
# print (df1[1][:])


# mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2
