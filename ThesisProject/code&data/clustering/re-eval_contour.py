import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from scipy.spatial import procrustes
import csv
import itertools as it
from copy import deepcopy

def resample(points,npoints):
    npots = np.shape(points)[0]
    newpots = np.zeros((npots,npoints,2))
    newpots_closed = np.zeros((npots,2*npoints-2,2))
    for i in range(npots):
        ind = np.max(np.where(points[i,:,0] != 0)[0])
        p = np.squeeze(points[i,:ind+1,:])
        dp = np.diff(p,axis=0)
        pts = np.zeros(len(dp)+1)
        pts[1:] = np.cumsum(np.sqrt(np.sum(dp*dp,axis=1)))
        newpts = np.linspace(0,pts[-1],npoints)
        newpots[i,:,0] = np.interp(newpts,pts,p[:,0])
        newpots[i,:,1] = np.interp(newpts,pts,p[:,1])
#         new_x = newpots[i,:,0] - np.min(newpots[i,:,0])
#         newpots_closed[i,:npoints,0] = new_x
#         newpots_closed[i,:npoints,1] = newpots[i,:,1]
#         newpots_closed[i,npoints:,0] = -1*new_x[::-1][1:-1]
#         newpots_closed[i,npoints:,1] = newpots[i,:,1][::-1][1:-1]
    return newpots

def procrustes_align(pots):
    newpots = np.zeros(np.shape(pots))
    for j in range(npots):
        mtx1, newpots[j,:,:], _ = procrustes(pots[0,:,:],pots[j,:,:])
    newpots[0,:,:] = mtx1
    # Scale to -1:1
    newpots[:,:,0] /= np.max(newpots[:,:,0])
    newpots[:,:,1] /= np.max(newpots[:,:,1])
    return newpots

pth = "contour_allmotif_190620/contour_csvs"
filenames = []
lengths = []

for file in os.listdir(pth):
    if file.endswith(".csv"):
        filenames.append(file)
        df = pd.read_csv(pth+"/"+file)
        x = df['x']
        lengths.append(len(x))


npots = len(filenames)
mx = max(lengths)
points = np.zeros((npots,mx,2))

for i in range(0,npots):
    df = pd.read_csv(pth+"/"+filenames[i])
    x = list(df['x'])
    y = list(df['y'])
    if y[0] > y[-1]:
        x.reverse()
        y.reverse()
        
    points[i,:len(x),0] = x
    points[i,:len(x),1] = y


# choose number
plt.axis([0, 8000, 0, 1])
plt.hist(lengths, weights=np.ones(len(lengths)) / len(lengths))
plt.show()

thresh = 1200
print(sum(i > thresh for i in lengths)/len(lengths))

# Desired number of points on each contour.
npoints = 1200
npots = np.shape(points)[0]

# Re-evaluate contours
newpots = resample(points,npoints)

# Procrustes Alignment
Ppots = procrustes_align(newpots)

nth = 22
fig,(ax1,ax2) = plt.subplots(1,2,figsize=(7,6))
ax1.plot(points[nth,:,0],points[nth,:,1],'-b')
ax1.set_title('Original Contour')
ax2.plot(newpots[nth,:,0],newpots[nth,:,1],'-r')
ax2.set_title('Re-evaluated Contour')



newpth = "contour_allmotif_190620/contour_csvs_resampled"


for i in range(0,npots):
    
    x = newpots[i,:,0]
    y = newpots[i,:,1]

    cont_coord = {}
    cont_coord['x'] = x
    cont_coord['y'] = y
    with open(newpth+"/"+filenames[i][:-4]+"_reeval.csv", "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(cont_coord.keys())
        writer.writerows(it.zip_longest(*cont_coord.values()))

