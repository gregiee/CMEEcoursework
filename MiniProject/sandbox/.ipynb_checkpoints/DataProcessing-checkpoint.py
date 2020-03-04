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
	# pick the min from the most continous
	startingPop = min(df.PopBio)
	# pick the max from the most continous
	carryingCapacity = max(df.PopBio)
	growthRate = []
	line = []
	# print(df)
	for i in range(len(df)-1) : 
		#dN = birth - death
		N1 = df.iloc[i, 1]
		N2 = df.iloc[i+1, 1]
		T1 = df.iloc[i, 0]
		T2 = df.iloc[i+1, 0]
		dN = N2-N1
		dT = T2-T1
		# print(dN)
		# print(dT)
		# print("-------")
		#rate = (1/N1)*(dN/dT)
		# rate = dN/dT
		#rate = dN
		#rate = dN*(1-(N1/carryingCapacity))
		#rate = (dN/dT)/(N1*((carryingCapacity-N1)/carryingCapacity))
		rate = (carryingCapacity*dN)/((carryingCapacity*N1-N1**2)*dT)
		growthRate.append(rate)
		tlag = T1 - N1 / rate
		line.append([rate,N1,T1,tlag])
	# print('growthRate')
	# print(growthRate)
	# try maybe top 5, not only the max?
	# print(growthRate)
	# growthRate.sort()
	line.sort()
	# print(line)
	if math.isinf(max(growthRate)):
		maxGrowthRate = line[-2][0]
		lag = line[-2][3]
	else:
		maxGrowthRate = line[-1][0]
		lag = line[-1][3]
	# print(maxGrowthRate)
	A = math.log(carryingCapacity/startingPop)

	return startingPop, carryingCapacity, maxGrowthRate, lag, A

# startingPop = startingPop1
# carryingCapacity = carryingCapacity1
# maxGrowthRate = maxGrowthRate1*10
#ipdb.set_trace()
def logisticGrowth(t, N0, Nmax, rmax):
	# print(t)
	# print(N0)
	# print(Nmax)
	# print(rmax)
	# """1-d gaussian: gaussian(x, amp, cen, wid)"""
	return (N0 * Nmax * np.exp(rmax * t)) / (Nmax + N0 * (np.exp(rmax*t) - 1))

def gompertz(t, A, rmax, tlag):
	return (A * np.exp ( - np.exp ( rmax * math.e * ( tlag - t ) / A + 1 ) ) ) 


def polynomial(t, C0, C1, C2, C3):
	# print(t)
	# print(N0)
	# print(Nmax)
	# print(rmax)
	# """1-d gaussian: gaussian(x, amp, cen, wid)"""
	return (C0 + C1 * t + C2 * t ** 2 + C3 * t ** 3 )



pdf = matplotlib.backends.backend_pdf.PdfPages("output_all_2020_l-2.pdf")
file = open("scores_2020_l-2.txt","w") 
truecounter = 0
falsecounter = 0
for i in range(max(workingdf.ID)):
	#max(workingdf.ID)
	data_subset = workingdf.loc[workingdf.ID == i, ['Time', 'PopBio', 'Species', 'Medium', 'Temp', 'Citation', 'Rep']]
	data_subset = data_subset.sort_values(by ='Time')
	# print(data_subset)
	# ipdb.set_trace()
	startingPop, carryingCapacity, maxGrowthRate, lag, A = getStartValue(data_subset)
	logisticmodel = Model(logisticGrowth)
	polymodel = Model(polynomial)
	gompertzmodel = Model(gompertz)
	fig = plt.figure()
	x = data_subset.Time
	y = data_subset.PopBio
	# print(y)
	try:
		# print('try fitting')
		result = logisticmodel.fit(y, t=x, N0=startingPop, Nmax=carryingCapacity, rmax=maxGrowthRate)
		# result = gompertzmodel.fit(y, t=x, A=A, rmax=maxGrowthRate, tlag = lag)
		# result = polymodel.fit(y, t=x, C0 = 1, C1 = 1, C2 = 1, C3 = 1)
		if result.success:
			truecounter = truecounter + 1
		# print('done fitting')
		yInit = result.init_fit
		yBest = result.best_fit
		fig.suptitle(str(result.best_values)+"\n"+str(result.aic)+"\n"+str(data_subset.iloc[0, 2])+"\n"+str(data_subset.iloc[0, 3])+"\n"+str(data_subset.iloc[0, 4]), fontsize=8)
		plt.plot(x, y, 'bo')
		plt.plot(x, yInit, 'r--', label='initial fit')
		plt.plot(x, yBest, 'r-', label='best fit')
		plt.legend(loc='best')
		# plt.savefig("../Results/"+str(i)+".pdf")
		# plt.close()
		pdf.savefig(fig)
		file.writelines("==ID: "+str(i))
		file.writelines("\n\nstarting value: N0"+str(startingPop)+", \nK"+str(carryingCapacity)+", \nRmax"+str(maxGrowthRate))
		file.writelines("\n\nbest value:")
		file.writelines(str(result.best_values))
		file.writelines(str(result.aic)+"\n\n")
		file.writelines("\n\nfit:")
		file.writelines(str(result.success)+"\n\n")
		# # print(min(x))
		print("\n\n\n==ID: "+str(i))
		print("====Fit:"+str(result.success))
		# # print(result.fit_report())
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


# # #ipdb.set_trace()


# pdf = matplotlib.backends.backend_pdf.PdfPages("output_all_2020_g.pdf")
# file = open("scores_2020_g.txt","w") 
# truecounter = 0
# falsecounter = 0
# for i in range(10):
# 	#max(workingdf.ID)
# 	data_subset = workingdf.loc[workingdf.ID == i, ['Time', 'PopBio', 'Species', 'Medium', 'Temp', 'Citation', 'Rep']]
# 	data_subset = data_subset.sort_values(by ='Time')
# 	# print(data_subset)
# 	# ipdb.set_trace()
# 	startingPop, carryingCapacity, maxGrowthRate, lag = getStartValue(data_subset)
# 	popGRmodel = Model(popGrowthCurve)
# 	polymodel = Model(polynomial)
# 	Gompertzmodel = Model(Gompertz)
# 	fig = plt.figure()
# 	x = data_subset.Time
# 	y = data_subset.PopBio
# 	A = math.log(carryingCapacity/startingPop)
# 	# print(y)
# 	# print('try fitting')
# 	# result = popGRmodel.fit(y, t=x, N0=startingPop, Nmax=carryingCapacity, rmax=maxGrowthRate)
# 	result = Gompertzmodel.fit(y, t=x, A = A, rmax=maxGrowthRate, tlag=lag)
# 	# result = polymodel.fit(y, t=x, C0 = 1, C1 = 1, C2 = 1, C3 = 1)
# 	if result.success:
# 		truecounter = truecounter + 1
# 	# print('done fitting')
# 	yInit = result.init_fit
# 	yBest = result.best_fit
# 	fig.suptitle(str(result.best_values)+str(result.aic)+str(data_subset.iloc[0, 2])+"\n"+str(data_subset.iloc[0, 3])+"\n"+str(data_subset.iloc[0, 4]), fontsize=8)
# 	plt.plot(x, y, 'bo')
# 	plt.plot(x, yInit, 'r--', label='initial fit')
# 	plt.plot(x, yBest, 'r-', label='best fit')
# 	plt.legend(loc='best')
# 	# plt.savefig("../Results/"+str(i)+".pdf")
# 	# plt.close()
# 	pdf.savefig(fig)
# 	file.writelines("==ID: "+str(i))
# 	file.writelines("\n\nstarting value: N0"+str(startingPop)+", K"+str(carryingCapacity)+", Rmax"+str(maxGrowthRate))
# 	file.writelines("\n\nbest value:")
# 	file.writelines(str(result.best_values))
# 	file.writelines(str(result.aic)+"\n\n")
# 	file.writelines("\n\nfit:")
# 	file.writelines(str(result.success)+"\n\n")
# 	# # print(min(x))
# 	print("\n\n\n==ID: "+str(i))
# 	print("====Fit:"+str(result.success))
# 	# # print(result.fit_report())
# 	# print(x)
# 	# print(y)
# 	# print(yInit)
# 	# print(yBest)
# 	# print(startingPop)
# 	# print(carryingCapacity)
# 	# print(maxGrowthRate)
# file.writelines("\n\ntruecounter: " + str(truecounter))
# file.writelines("\n\nfalsecounter: " + str(falsecounter))
# pdf.close()
# file.close()

# # #calculate delta AIC(c), weighted AIC(c)==2,2-4,4-10, find the smaller one
# # plt.plot(data_subset['Time'], data_subset['PopBio'], 'bo')
# # plt.plot(data_subset['Time'], result.init_fit, 'r--', label='initial fit')
# # plt.plot(data_subset['Time'], result.best_fit, 'r-', label='best fit')
# # # plt.plot(data_subset['Time'], result1.init_fit, 'g--', label='initial fit1')
# # # plt.plot(data_subset['Time'], result1.best_fit, 'g-', label='best fit1')
# # plt.legend(loc='best')
# # plt.show()


# #ipdb.set_trace()
