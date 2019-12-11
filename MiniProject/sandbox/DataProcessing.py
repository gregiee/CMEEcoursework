#!/usr/bin/env python3
"""mini project"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import re
import ipdb
import pandas as pd 
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt
#from lmfit import minimize, Parameters
from lmfit import Model
from operator import itemgetter
import matplotlib.backends.backend_pdf


RawData = pd.read_csv("../Data/LogisticGrowthData.csv")
#MetaData = pd.read_csv("../Data/LogisticGrowthMetaData.csv")
workingdf = RawData[RawData.PopBio > 0]
workingdf = workingdf.assign(ID=(workingdf.Species + '_' + workingdf.Temp.map(str) + "_" + workingdf.Medium + "_" + workingdf.Citation +"_" + workingdf.Rep.map(str)).astype('category').cat.codes)

#test out with id group 94
#get subset/read csv
#ipdb.set_trace()
#get innitial values, using a function
def getStartValue(df):
	startingPop = min(df.PopBio)
	carryingCapacity = max(df.PopBio)
	growthRate = []
	for i in range(len(df)-1) : 
		#dN = birth - death
		N1 = df.iloc[i, 1]
		N2 = df.iloc[i+1, 1]
		T1 = df.iloc[i, 0]
		T2 = df.iloc[i+1, 0]
		dN = N1-N2
		dT = T1-T2
		#rate = (1/N1)*(dN/dT)
		rate = dN/dT
		#rate = dN
		#rate = dN*(1-(N1/carryingCapacity))
		growthRate.append(rate)
	print('growthRate')
	print(growthRate)
	maxGrowthRate = max(growthRate)
	return startingPop, carryingCapacity, maxGrowthRate

# startingPop = startingPop1
# carryingCapacity = carryingCapacity1
# maxGrowthRate = maxGrowthRate1*10
#ipdb.set_trace()
def popGrowthCurve(t, N0, Nmax, rmax):
	print(t)
	print(N0)
	print(Nmax)
	print(rmax)
	"""1-d gaussian: gaussian(x, amp, cen, wid)"""
	return (N0 * Nmax * np.exp(rmax * t)) / (Nmax + N0 * (np.exp(rmax*t) - 1))

pdf = matplotlib.backends.backend_pdf.PdfPages("output_all.pdf")
file = open("scores.txt","w") 
truecounter = 0
falsecounter = 0
for i in range(18,19):
	#look at error file, too many points???.
	#max(workingdf.ID)
	data_subset = workingdf.loc[workingdf.ID == i, ['Time', 'PopBio', 'Species', 'Medium', 'Temp', 'Citation', 'Rep']]
	data_subset = data_subset.sort_values(by ='Time')
	# print(data_subset)
	# ipdb.set_trace()
	startingPop, carryingCapacity, maxGrowthRate = getStartValue(data_subset)
	popGRmodel = Model(popGrowthCurve)
	fig = plt.figure()
	x = data_subset.Time
	y = data_subset.PopBio
	try:
		# print('try fitting')
		result = popGRmodel.fit(y, t=x, N0=startingPop, Nmax=carryingCapacity, rmax=maxGrowthRate)
		truecounter = truecounter + 1
		# print('done fitting')
		yInit = result.init_fit
		yBest = result.best_fit
		fig.suptitle(str(result.best_values)+str(result.aic)+str(data_subset.iloc[0, 2])+"\n"+str(data_subset.iloc[0, 3])+"\n"+str(data_subset.iloc[0, 4]), fontsize=8)
		plt.plot(x, y, 'bo')
		plt.plot(x, yInit, 'r--', label='initial fit')
		plt.plot(x, yBest, 'r-', label='best fit')
		plt.legend(loc='best')
		# plt.savefig("../Results/"+str(i)+".pdf")
		# plt.close()
		pdf.savefig(fig)
		file.writelines("==ID: "+str(i))
		file.writelines(str(result.best_values))
		file.writelines(str(result.aic)+"\n\n")
		# print(min(x))
		print("\n\n\n==ID: "+str(i))
		print("====Fit:"+str(result.success))
		# print(result.fit_report())
		# print(x)
		# print(y)
		# print(yInit)
		# print(yBest)
		# print(startingPop)
		# print(carryingCapacity)
		# print(maxGrowthRate)
	except ValueError as e:
		falsecounter = falsecounter + 1
		#print('in except')
		fig.suptitle(str(data_subset.iloc[0, 2])+"\n"+str(data_subset.iloc[0, 3])+"\n"+str(data_subset.iloc[0, 4]), fontsize=8)
		plt.plot(x, y, 'bo')
		pdf.savefig( fig )
		# print(x)
		# print(startingPop)
		# print(carryingCapacity)
		# print(maxGrowthRate)
		file.writelines("fffffffffff==ID: "+str(i))
		print("\n\n\n==ID: "+str(i))
		print("====Fit: Failed")
		print(e)
		pass
file.writelines("\n\ntruecounter: " + str(truecounter))
file.writelines("\n\nfalsecounter: " + str(falsecounter))
pdf.close()
file.close()

# #calculate delta AIC(c), weighted AIC(c)==2,2-4,4-10, find the smaller one
# plt.plot(data_subset['Time'], data_subset['PopBio'], 'bo')
# plt.plot(data_subset['Time'], result.init_fit, 'r--', label='initial fit')
# plt.plot(data_subset['Time'], result.best_fit, 'r-', label='best fit')
# # plt.plot(data_subset['Time'], result1.init_fit, 'g--', label='initial fit1')
# # plt.plot(data_subset['Time'], result1.best_fit, 'g-', label='best fit1')
# plt.legend(loc='best')
# plt.show()


#ipdb.set_trace()
