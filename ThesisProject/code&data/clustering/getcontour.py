import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu
from skimage import measure
import os
import itertools as it
import csv
from skimage import data, img_as_float,io
from copy import deepcopy
from skimage.transform import rescale, resize
import warnings
warnings.filterwarnings("ignore")

def get_outline_contour(img,position):
    # Input: grey-scaled image of motif, position of motif in image e.g. left,right, or "longest" for longest contour. 
    # Output: contour of desired motif.
    # Note: if there's only one motif in the image, use position="longest".
    
    # Get all contours:
    thresh = threshold_otsu(img)
    binary = img > thresh
    cont = measure.find_contours(binary, 0.8)
    
    # Compute lengths of contours:
    cont_ln = []
    for n, contour in enumerate(cont):
        cont_ln.append(len(contour))
        
    if position == "longest":
        k = np.argmax(cont_ln)
        contour = cont[k]
    
    else:
        # Find longest contours:
        longest_c = sorted(cont_ln,reverse=True)[:2] # Assuming there are no more than 2 motif views in one image
        long_ind = []
        minx = []
        for i in range(0,len(cont_ln)):
            if cont_ln[i] in longest_c:
                long_ind.append(i)
                c = cont[i]
                x = c[:,1]
                minx.append(min(x))

        if "left" in position:
            contour = cont[long_ind[np.argmin(minx)]]
        else:
            # if we're looking for the right-most contour
            contour = cont[long_ind[np.argmax(minx)]]        
            
    return contour

def binarize_motif(img):
    # Input: coloured image
    # Output: edited image that has either black or white pixels.
    
    # 1) Get image size
    ###################
    x_len = len(img[0])
    y_len = len(img)
    img2 = deepcopy(img)

    # 2) Binarize image
    ###################
    # Pixels that are not white will be turned black, all other pixels will be turned white.
    for i in range(0,y_len):
        for j in range(0,x_len):
            if sum(img[i][j]) <= 755:
                img2[i][j] = [0,0,0]
            else:
                img2[i][j] = [255,255,255]


    return img2

# 1) Speciy folders:
img_pth = "merged" # this is where the original images are located.
cont_plots = "contour_plots" # the folder to save contour plots.
cont_csvs = "contour_csvs" # the folder to save contour csvs in.
b_img = "b_img"
counter = 0
# 2) Iterate through motifs in folder:
for motif in os.listdir(img_pth):

    print(str(counter)+"/"+str(len(os.listdir(img_pth))))
    try:
        # 2.1. Load grey-scaled image
        image = io.imread(img_pth+"/"+motif,as_gray=False) # Here, we load a grey-scaled version of the image.
        if image.shape[0] > 1000:
            image = np.round(
                    rescale(image, 1000 / (image.shape[0] * 1.0), preserve_range=True, multichannel=True)
            ).astype('uint8')
        elif image.shape[1] > 1000:
            image = np.round(
                    rescale(image, 1000 / (image.shape[1] * 1.0), preserve_range=True, multichannel=True)
            ).astype('uint8')
        image_bw = binarize_motif(image)
        io.imsave(b_img+"/"+motif, image_bw)  # We temporarily save image so we can load it again as a grey-scaled image.
        img_in_use = io.imread(b_img+"/"+motif, as_gray=True)
    except ValueError:
        print("check"+str(motif))
        counter = counter + 1
        continue
    # 2.2. Find contour
    try:
        contour = get_outline_contour(img_in_use,"longest")
        x = contour[:,1]
        y = contour[:,0]
        
        # 2.3. Save Plot
        fig, ax = plt.subplots(figsize=(6, 8))
        plt.gray()
        ax.imshow(image,cmap='gray')
        ax.plot(x,y,'-r',linewidth=2)
        ax.set_axis_off()
        plt.savefig(cont_plots+"/"+motif,bbox_inches = 'tight',pad_inches=0.0)
        plt.close()
        
        # 2.4. Save CSV
        
        cont_coord = {}
        cont_coord['x'] = x
        cont_coord['y'] = y
        with open(cont_csvs+"/"+motif[:-3]+"csv", "w", newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(cont_coord.keys())
            writer.writerows(it.zip_longest(*cont_coord.values()))
        counter = counter + 1
    except ValueError:
        print("check"+str(motif))
        counter = counter + 1

