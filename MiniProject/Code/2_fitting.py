#!/usr/bin/env python3
"""mini project"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

# Opens the (new, modified) dataset from previous step.

# Calculates starting values).

# !!Obtaining starting values
# A good strategy to optimize fits is to not sample starting values from a distribution. 
# For example, you can choose a gaussian (high confidence in mean of parameter) 
# or a uniform distribution (low confidence in mean, high confidence in the range of values that the parameter can take) 
# with the mean being the value you inferred from the data.

# Does the NLLS fitting.

# Uses the try construct because not all runs will converge: for Python, see this; for R, recall this. The more data curves you are able to fit, the better — that is part of the challenge

# Calculates AIC, BIC, R2, and other statistical measures of model fit (you decide what you want to include)

# Exports the results to a csv that the final plotting script can read.

# loading packages
import pandas as pd 
import math
import numpy as np
from lmfit import Model, Parameters
import random
import warnings

#ignore by message
warnings.filterwarnings("ignore", message="divide by zero encountered")
warnings.filterwarnings("ignore", message="overflow encountered in exp")

# starting value function 
def getStartValue(df):
    """getting starting value"""
    # pick the min from the most continous
    startingPop = min(df.logPopBio)
    # pick the max from the most continous
    carryingCapacity = max(df.logPopBio)
    growthRate = []
    line = []
    for i in range(len(df)-1) :
        N1 = df.iloc[i, 1]
        N2 = df.iloc[i+1, 1]
        T1 = df.iloc[i, 0]
        T2 = df.iloc[i+1, 0]
        dN = N2-N1
        dT = T2-T1
        rate = dN/dT
        growthRate.append(rate)
        tlag = T1 - N1 / rate + startingPop
        line.append([rate,N1,T1,tlag])
    line.sort()
    if math.isinf(max(growthRate)):
        maxGrowthRate = line[-2][0]
        lag = line[-2][2] + (startingPop - line[-2][1]) / maxGrowthRate
    else:
        maxGrowthRate = line[-1][0]
        lag = line[-1][2] + (startingPop - line[-1][1]) / maxGrowthRate
    return startingPop, carryingCapacity, maxGrowthRate, lag

# r2 function
def R2(ssr, sse):
    """getting r2"""    
    r2 = []
    for i in range(len(ssr)):
        if ssr[i] == "NA":
            r2.append("NA")
        else:
            rsquare = 1 - ssr[i]/sse[i]
            r2.append(rsquare)
    return r2

# models
def logisticGrowth(t, N0, Nmax, rmax):
    """logistic model"""
    return (N0 * Nmax * np.exp(rmax * t)) / (Nmax + N0 * (np.exp(rmax*t) - 1))

def logisticGrowthlag(t, N0, Nmax, rmax, tlag):
    """logistic model with tlag"""
    return N0 + (Nmax - N0) / (1 + np.exp(4 * rmax * (tlag - t) / (Nmax - N0) + 2))

def gompertz(t, N0, Nmax, rmax, tlag):
    """gompertz model"""
    return ((Nmax - N0) * np.exp ( - np.exp ( rmax * math.e * ( tlag - t ) / (Nmax - N0) + 1 ) ) ) + N0

def baranyi(t, N0, Nmax, rmax, tlag):
    """baranyi model"""
    return Nmax + np.log((-1 + np.exp(rmax * tlag) + np.exp(rmax * t)) / (np.exp(rmax * t) - 1 + np.exp(rmax * tlag) * np.exp(Nmax - N0)))

def polynomial(t, C0, C1, C2, C3):
    """polynomial model"""
    return (C0 + C1 * t + C2 * t ** 2 + C3 * t ** 3 )


# load processed data
workingdf = pd.read_csv("../Data/workingdf.csv")

# initiate storage data frame
graphdf = pd.DataFrame()
analysisdf = workingdf[["ID", "Temp", "Medium", "Species"]].drop_duplicates().sort_values(by=["ID"])

# begin fitting
whole = len(workingdf.ID.unique())
# initiate storage
lAIC, lBIC, lSSR = [], [], []
pAIC, pBIC, pSSR = [], [], []
gAIC, gBIC, gSSR = [], [], []
bAIC, bBIC, bSSR = [], [], []
SSE = []
deathPhase = [] 
print("fitting data set group and saving results, it might take a few minutes(~5)...")
    
for i in range(whole):
    if (i % 10 == 0 ):
        print("fitting set "+str(i)+" to "+str(i+9))
    data_subset = workingdf.loc[workingdf.ID == i, ['Time', 'logPopBio', 'Species', 'Medium', 'Temp', 'Citation', 'Rep']]
    data_subset = data_subset.sort_values(by ='Time')
    startingPop, carryingCapacity, maxGrowthRate, lag = getStartValue(data_subset)
    
    logisticmodel = Model(logisticGrowthlag)
    polymodel = Model(polynomial)
    gompertzmodel = Model(gompertz)
    baranyimodel = Model(baranyi)
    subsetCount = len(data_subset.Time)
    x = data_subset.Time
    y = data_subset.logPopBio
    meanY = np.mean(y)
    IDList = [i]*len(data_subset.Time)
    xList = list(x)
    yList = list(y)
    d = (max(yList) - yList[-1])/(max(yList)-min(yList))
    if d > 0.2:
        deathPhase.append(1)
    else:
        deathPhase.append(0)
    
    logisticFitList, polyFitList, gompertzFitList, baranyiFitList, NAList = [], [], [], [], ['NA']*subsetCount
    params = Parameters()
    params.add('N0', value=startingPop)
    params.add('Nmax', value=carryingCapacity)
    params.add('rmax', value=maxGrowthRate)
    params.add('tlag', value=lag)
    try:
        result = logisticmodel.fit(y, params, t=x)
        if result.success:
            yFit = result.best_fit
            logisticFitList = list(yFit)
            lAIC.append(result.aic)
            lBIC.append(result.bic)
            lSSR.append(sum(map(lambda x: x*x, result.residual)))
        else:
            logisticFitList = NAList
            lAIC.append("NA")
            lBIC.append("NA")
            lSSR.append("NA")
    except ValueError as e:
        logisticFitList = NAList
        lAIC.append("NA")
        lBIC.append("NA")
        lSSR.append("NA")
        pass

    
    try:
        result = polymodel.fit(y, t=x, C0 = 1, C1 = 1, C2 = 1, C3 = 1)
        if result.success:
            yFit = result.best_fit
            polyFitList = list(yFit)
            pAIC.append(result.aic)
            pBIC.append(result.bic)
            pSSR.append(sum(map(lambda x: x*x, result.residual)))
        else:
            polyFitList = NAList
            pAIC.append("NA")
            pBIC.append("NA")
            pSSR.append("NA")
    except ValueError as e:
        polyFitList = NAList
        pAIC.append("NA")
        pBIC.append("NA")
        pSSR.append("NA") 
        pass
    
    
    try:
        result = gompertzmodel.fit(y, params, t=x)
        if result.success:
            yFit = result.best_fit
            gompertzFitList = list(yFit)
            gAIC.append(result.aic)
            gBIC.append(result.bic)
            gSSR.append(sum(map(lambda x: x*x, result.residual)))
        else:
            gompertzFitList = NAList
            gAIC.append("NA")
            gBIC.append("NA")
            gSSR.append("NA")
    except ValueError as e:
        gompertzFitList = NAList
        gAIC.append("NA")
        gBIC.append("NA")
        gSSR.append("NA")
        pass
    
    
    try:
        result = baranyimodel.fit(y, params, t=x)
        if result.success:
            yFit = result.best_fit
            baranyiFitList = list(yFit)
            bAIC.append(result.aic)
            bBIC.append(result.bic)
            bSSR.append(sum(map(lambda x: x*x, result.residual)))
        else:
            print("improving starting values since fit failed")
            attamptcount = 0
            while(not result.success and attamptcount < 10):
                attamptcount += 1
                params.add('rmax', value=random.uniform(maxGrowthRate/3,maxGrowthRate))
                result = baranyimodel.fit(y, params, t=x)
            if result.success:
                yFit = result.best_fit
                baranyiFitList = list(yFit)
                bAIC.append(result.aic)
                bBIC.append(result.bic)
                bSSR.append(sum(map(lambda x: x*x, result.residual)))
            else:
                baranyiFitList = NAList
                bAIC.append("NA")
                bBIC.append("NA")
                bSSR.append("NA")
    except ValueError as e:
        baranyiFitList = NAList
        bAIC.append("NA")
        bBIC.append("NA")
        bSSR.append("NA")
        pass
    SSE.append(sum(map(lambda x: (x-meanY)**2, y)))
    tempdf = pd.DataFrame({"ID":IDList,
                           "x":xList,
                           "y":yList,
                           "logisticFit":logisticFitList,
                           "polyFit":polyFitList,
                           "gompertzFit":gompertzFitList,
                           "baranyiFit":baranyiFitList,
                          })
    graphdf = graphdf.append(tempdf, ignore_index=True)

# populate analysis dataframe
analysisdf = analysisdf.assign(lAIC = lAIC, lBIC = lBIC, lR2 = R2(lSSR,SSE), 
                               pAIC = pAIC, pBIC = pBIC, pR2 = R2(pSSR,SSE), 
                               gAIC = gAIC, gBIC = gBIC, gR2 = R2(gSSR,SSE), 
                               bAIC = bAIC, bBIC = bBIC, bR2 = R2(bSSR,SSE),
                              deathPhase = deathPhase)

# save dataframe
graphdf.to_csv('../Data/graphdf.csv', index=False)
analysisdf.to_csv('../Data/analysisdf.csv', index=False)
