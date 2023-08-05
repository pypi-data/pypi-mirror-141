#Submitted By:
#Aastha Jaipuria 101903306 3CO12

import sys
import os
import pathlib
import pandas as pd
import numpy as np
import math


#The cmd line args will be like <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>
# ie. 101903306.py 101903306-data.csv "1,1,2,1,2" "+,+,-,+,-" 101903306-result.csv

#We should have 5 arguments.
if len(sys.argv)!=5:
    sys.exit("ERROR: Enter correct number of parameters")

try:
    f = open(sys.argv[1], 'r')
except (FileNotFoundError, IOError):
    sys.exit("ERROR: File not Found")

if pathlib.Path(sys.argv[1]).suffix!=".csv" and pathlib.Path(sys.argv[1]).suffix!=".xlsx":
    sys.exit("Not a csv or xlsx file")

val = sys.argv[1]
try:
    val = float(val)
except:
    if type(val)!=type('str'):
        sys.exit("File name is not correct")

#Now check if we have 3 or more than 3 columns in input file
df = pd.read_excel(sys.argv[1])
if df.shape[1]<3:
    sys.exit("Atleast 3 columns should be there.")

weights = sys.argv[2]
impacts = sys.argv[3]

weights = weights.split(",")
impacts = impacts.split(",")

for i in weights:
    if i.isnumeric() == False:
        sys.exit("ERROR: Weights should be numeric.")

for i in impacts:
    if i!="+" and i!="-":
        sys.exit("ERROR: impacts should either be + or -")

if df.shape[1]-1 != len(weights) or len(weights)!=len(impacts):
    sys.exit("No. of weights, impacts and cols must be same.")

outputFile = sys.argv[4]

columns = list(df)[1:]
for col in columns:
    if not pd.api.types.is_integer_dtype(df[col].dtypes) and not pd.api.types.is_float_dtype(df[col].dtypes):
        # print()
        raise Exception("ERROR: 2nd to last columns must contain numeric values only.")

#Now write the code for TOPSIS:

def topsis(DF, weights, impacts):
    df = DF.copy()
    #Step 1: Normalization
    df.set_index(df.columns[0], inplace=True)
    df = df/np.sqrt(np.power(df, 2).sum(axis=0)) #normalised decision matrix
    df = df*weights #weighted normalised decision matrix

    #Now calculate deal best and ideal worst
    idealBest = []
    idealWorst = []

    idx = 0
    for i in df.columns:
        if impacts[idx] == '+':
            idealBest.append(df[i].max())
            idealWorst.append(df[i].min())
        else:
            idealBest.append(df[i].min())
            idealWorst.append(df[i].max())
        idx+=1

    #Now calculate Eucledian distance from ideal best value and ideal worst value
    distBest = np.sqrt(np.power(df-idealBest, 2).sum(axis=1))
    distWorst = np.sqrt(np.power(df-idealWorst, 2)).sum(axis=1)
    
    #Calculate Performance Score
    PerformanceScore = distWorst/(distBest+distWorst)
    
    #Now find rank
    Rank = PerformanceScore.rank(ascending = False)
    Rank = [int(i) for i in Rank]
    DF['Score'] = list(PerformanceScore)
    DF['Rank'] = Rank

weights = [float(i) for i in weights]
topsis(df, weights, impacts)
df.to_csv(outputFile)


