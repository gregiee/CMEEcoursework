# import pcks
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
from scipy.spatial import procrustes
%matplotlib inline


testfull = pd.read_csv("contourc1.csv")
aaa = testfull[["x","y"]].to_numpy()
bbb, ccc = [], []
counter = 0
for x in aaa:
    ccc.append(list(x))
    counter = counter + 1
    if counter >= 240:
        bbb.append(ccc)
        ccc = []
        counter = 0
newdatamatrix = np.asarray(bbb, float)
nshapes, npoints, blah = np.shape(newdatamatrix)
datamatrix = newdatamatrix.reshape([nshapes,npoints*2])
C = np.cov(datamatrix.T)
evals,evecs = np.linalg.eig(C)
indices = np.argsort(evals)
indices = indices[::-1]
evecs = evecs[:,indices]
evals = evals[indices]
evecs = np.real(evecs)
evals = np.real(evals)
m = np.mean(datamatrix,axis=0)
mplot = m.reshape((npoints,2))
evecsplot = evecs.reshape((npoints,2,npoints*2))
sd = 3
pc = 0
pl.plot(mplot[:,0],mplot[:,1],'b')
pl.plot(mplot[:,0] - np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] - np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 
pl.plot(mplot[:,0] + np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] + np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 


testfull = pd.read_csv("contourc2.csv")
aaa = testfull[["x","y"]].to_numpy()
bbb, ccc = [], []
counter = 0
for x in aaa:
    ccc.append(list(x))
    counter = counter + 1
    if counter >= 240:
        bbb.append(ccc)
        ccc = []
        counter = 0
newdatamatrix = np.asarray(bbb, float)
nshapes, npoints, blah = np.shape(newdatamatrix)
datamatrix = newdatamatrix.reshape([nshapes,npoints*2])
C = np.cov(datamatrix.T)
evals,evecs = np.linalg.eig(C)
indices = np.argsort(evals)
indices = indices[::-1]
evecs = evecs[:,indices]
evals = evals[indices]
evecs = np.real(evecs)
evals = np.real(evals)
m = np.mean(datamatrix,axis=0)
mplot = m.reshape((npoints,2))
evecsplot = evecs.reshape((npoints,2,npoints*2))
sd = 3
pc = 0
pl.plot(mplot[:,0],mplot[:,1],'b')
pl.plot(mplot[:,0] - np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] - np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 
pl.plot(mplot[:,0] + np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] + np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 


testfull = pd.read_csv("contourc3.csv")
aaa = testfull[["x","y"]].to_numpy()
bbb, ccc = [], []
counter = 0
for x in aaa:
    ccc.append(list(x))
    counter = counter + 1
    if counter >= 240:
        bbb.append(ccc)
        ccc = []
        counter = 0
newdatamatrix = np.asarray(bbb, float)
nshapes, npoints, blah = np.shape(newdatamatrix)
datamatrix = newdatamatrix.reshape([nshapes,npoints*2])
C = np.cov(datamatrix.T)
evals,evecs = np.linalg.eig(C)
indices = np.argsort(evals)
indices = indices[::-1]
evecs = evecs[:,indices]
evals = evals[indices]
evecs = np.real(evecs)
evals = np.real(evals)
m = np.mean(datamatrix,axis=0)
mplot = m.reshape((npoints,2))
evecsplot = evecs.reshape((npoints,2,npoints*2))
sd = 3
pc = 0
pl.plot(mplot[:,0],mplot[:,1],'b')
pl.plot(mplot[:,0] - np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] - np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 
pl.plot(mplot[:,0] + np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] + np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 


testfull = pd.read_csv("contourc4.csv")
aaa = testfull[["x","y"]].to_numpy()
bbb, ccc = [], []
counter = 0
for x in aaa:
    ccc.append(list(x))
    counter = counter + 1
    if counter >= 240:
        bbb.append(ccc)
        ccc = []
        counter = 0
newdatamatrix = np.asarray(bbb, float)
nshapes, npoints, blah = np.shape(newdatamatrix)
datamatrix = newdatamatrix.reshape([nshapes,npoints*2])
C = np.cov(datamatrix.T)
evals,evecs = np.linalg.eig(C)
indices = np.argsort(evals)
indices = indices[::-1]
evecs = evecs[:,indices]
evals = evals[indices]
evecs = np.real(evecs)
evals = np.real(evals)
m = np.mean(datamatrix,axis=0)
mplot = m.reshape((npoints,2))
evecsplot = evecs.reshape((npoints,2,npoints*2))
sd = 3
pc = 0
pl.plot(mplot[:,0],mplot[:,1],'b')
pl.plot(mplot[:,0] - np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] - np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 
pl.plot(mplot[:,0] + np.sqrt(evals[pc])*sd*evecsplot[:,0,pc], mplot[:,1] + np.sqrt(evals[pc])*sd*evecsplot[:,1,pc],'r') 
