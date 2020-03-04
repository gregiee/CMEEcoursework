#!/usr/bin/env python3
"""mini project"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

# Creates unique ids so that you can identify unique datasets
# Filters out datasets with less than x data points, where x is the minimum number of data points needed to fit the models. 
# Note that this step is not necessary because in any case, the model fitting (or estimation of goodness of fit statistics) will fail for datasets with small sample sizes anyway, and you can then filter these datasets after the NLLS fitting script (see below) has finished running and you are in the analysis phase.
# Deals with missing, and other problematic data values.
# Saves the modified data to one or more csv file(s)

# loading packages
import pandas as pd 
import math
import numpy as np

# load raw data
RawData = pd.read_csv("../Data/LogisticGrowthData.csv")

# assign unique id based on different filters
workingdf = RawData.assign(ID=(RawData.Species + '_' + RawData.Temp.map(str) + "_" + RawData.Medium + "_" + 
                               RawData.Citation +"_" + RawData.Rep.map(str)).astype('category').cat.codes)

# apply filters to deal with negative value, missing value, etc.
# NAs
if workingdf.Time.isnull().sum() != 0:
    workingdf = workingdf.dropna()
    
if workingdf.PopBio.isnull().sum() != 0:
    workingdf = workingdf.dropna()
    
# negatives
timeNegArray = workingdf.loc[workingdf['Time']<0].sort_values(by=['Time'])["ID"].unique()
popNegArray = workingdf.loc[workingdf['Time']<0].sort_values(by=['PopBio'])["ID"].unique()
# shifting neg time
if timeNegArray.any():
    for i in range(len(timeNegArray)):
        target = timeNegArray[i]
        tMin = min(workingdf.loc[workingdf.ID == target, "Time"])
        workingdf.loc[workingdf.ID == target, "Time"] = workingdf.loc[workingdf.ID == target, "Time"] + abs(tMin)
# shifting neg pop
if popNegArray.any():
    for i in range(len(popNegArray)):
        target = popNegArray[i]
        pMin = min(workingdf.loc[workingdf.ID == target, "PopBio"])
        workingdf.loc[workingdf.ID == target, "PopBio"] = workingdf.loc[workingdf.ID == target, "PopBio"] + abs(pMin)
        
# getting rid of 0 in Pop and adding logged data to dataframe
workingdf = workingdf[workingdf.PopBio > 0]
workingdf.loc[workingdf.PopBio > 0, "logPopBio"] = np.log(workingdf.loc[workingdf.PopBio > 0, "PopBio"])

# save df to csv
workingdf.to_csv('../Data/workingdf.csv', index=False)