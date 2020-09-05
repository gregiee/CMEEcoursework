from skimage import data, io, filters, img_as_uint, img_as_float, img_as_ubyte
import random, os

from PIL import Image, ImageFont, ImageDraw, ImageEnhance

# http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_label.html
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border, find_boundaries
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing, binary_dilation, binary_erosion, square, selem
from skimage.color import label2rgb
from skimage.transform import rescale, resize
from scipy.ndimage import binary_fill_holes
from skimage.color import rgb2gray

import sklearn
from sklearn.model_selection import train_test_split

from os import listdir
from os.path import isfile, join, exists
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

%matplotlib inline

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

def read_csv_roster(roster_path, columns_to_drop=[]):
    print(exists(roster_path))
    assert(exists(roster_path))
    try: 
        roster = pd.read_csv(roster_path)
    except: 
        raise ValueError('file could not read.')
    roster.drop(columns=columns_to_drop, inplace=True)
    roster.dropna(axis=0, how='all', inplace=True)
    return roster

def get_only_given_motifs(roster, motif_names=[]):
    for motif in motif_names:
        roster.drop(roster[roster[motif] == 0].index, inplace=True)
    return roster

def read_dirs(input_dir):
    assert(exists(input_dir))
    return listdir(input_dir)

def read_files(input_dir):
    assert(exists(input_dir))
    files = []
    for f in listdir(input_dir):
        files.append(f)
    return files

def read_file_names_only(input_dir):
    assert(exists(input_dir))
    files = []
    for f in listdir(input_dir):
        files.append(f[:f.find('.')])
    return files

def compare_roster_dataset_for_missing_items(ids_from_roster, ids_from_dataset):
    not_in_dataset_but_on_roster = []
    print('not_in_dataset_but_on_roster:')
    for id_ in ids_from_roster:
        if not id_ in ids_from_dataset:
            print(id_)
            not_in_dataset_but_on_roster.append(id_)
    
    print('not_on_roster_but_in_dataset:')
    not_on_roster_but_in_dataset = []
    for id_ in ids_from_dataset:
        if not id_ in ids_from_roster:
            print(id_)
            not_on_roster_but_in_dataset.append(id_)
            
    return not_in_dataset_but_on_roster, not_on_roster_but_in_dataset


def get_valid_images(all_ids, file_dirs, exlude_from_list):
    valid_ids, invalid_ids = [], []
    for id_ in all_ids:
        if id_ in exlude_from_list:
            continue
        elif id_ in file_dirs:
            valid_ids.append(id_)
        else:
            invalid_ids.append(id_)
            
    if len(valid_ids) == len(all_ids):
        print('Yay, all the images on roster have segmentations in dataset!')
        
    return valid_ids, invalid_ids


def parse_image_name(image_name):
    beg = image_name.find('_')
    image_id = image_name[:beg] 
    motif_id = image_name[beg+1:image_name.find('_', beg+1)]
    motif_type = image_name[image_name.find('.')-1]
    return image_id, motif_id, motif_type

def attempt_read_image(image_name_no_extension, image_dir):
    valid_name = image_name_no_extension + '.jpg'
    path = join(image_dir, valid_name)
    if not exists(path):
        valid_name = image_name_no_extension + '.JPG'
        path = join(image_dir, valid_name)
    if not exists(path):
        valid_name = image_name_no_extension + '.tiff'
        path = join(image_dir, valid_name)

    image = np.array(Image.open(path))
    return image, valid_name

def read_original_image(image_id, dataset_dir):
    valid_name = image_id + '.jpg'
    image_dir = join(dataset_dir, image_id)
    path = join(image_dir, valid_name)
    if not exists(path):
        valid_name = image_id + '.JPG'
        path = join(image_dir, valid_name)
    if not exists(path):
        valid_name = image_id + '.tiff'
        path = join(image_dir, valid_name)

    #image = io.imread(path)
    image = np.array(Image.open(path))
    return image, valid_name

def imshow(image):
    plt.figure(figsize=(18, 12))
    plt.imshow(image)
    
def show_image_alongside_others(image=None, mask=None, seg=None, save_name=None):
    fig1 = plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.imshow(image)
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(mask, cmap='spectral')
    plt.axis('off')
    plt.subplot(133)
    if not seg is None:
        plt.imshow(seg, cmap='spectral')
    else:
        plt.imshow(mask, cmap='spectral')
        
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    plt.draw()
    
    if not save_name == None:
        fig1.savefig(save_name, dpi=100)
        
def bwlabeln(main_image, seg_mask):
    blobs_labels = measure.label(seg_mask, neighbors=8, background=False)
    print(len(np.unique(blobs_labels)))

    colors = generate_colors(len(np.unique(blobs_labels))-1)
    colored_blobs = np.zeros(main_image.shape).astype(np.uint8)

    red = colored_blobs[:,:,0]
    blue = colored_blobs[:,:,1]
    green = colored_blobs[:,:,2]
    
    for i, rgb in enumerate(colors):
        red[blobs_labels == i+1] = rgb[0]
        green[blobs_labels == i+1] = rgb[1]
        blue[blobs_labels == i+1] = rgb[2]
    
    colored_blobs[:,:,0] = red
    colored_blobs[:,:,1] = blue
    colored_blobs[:,:,2] = green

    print(len(np.unique(colored_blobs)))
    #io.imsave('../data/out/VA1_masked_250_labeled.png', colored_blobs)
    return colored_blobs

def superimpose_image(image, mask_to_superimpose):
    mask = mask_to_superimpose > 0 # Binarize it
    superimposed = image.copy()

    red = superimposed[:,:,0]
    blue = superimposed[:,:,1]
    green = superimposed[:,:,2]

    red[mask == True] = 255
    green[mask == True] = 0
    blue[mask == True] = 0

    superimposed[:,:,0] = red
    superimposed[:,:,1] = blue
    superimposed[:,:,2] = green

    return superimposed

def postprocess_mask(mask, name):
    # Closing first
    if name in OPERATION_DICT.keys():
        if OPERATION_DICT[name]['operation'] == 'erosion_first':
            mask = binary_erosion(mask, selem=selem.diamond(OPERATION_DICT[name]['selem'][0]))
            mask = binary_dilation(mask, selem=selem.diamond(OPERATION_DICT[name]['selem'][1]))
        elif OPERATION_DICT[name]['operation'] == 'dilation_first':
            mask = binary_dilation(mask, selem=selem.diamond(OPERATION_DICT[name]['selem'][0]))
            mask = binary_erosion(mask, selem=selem.diamond(OPERATION_DICT[name]['selem'][1]))
    
    # Post process mask which only returns only one connected component
    label_mask = label(mask, neighbors=8, background=False)

    # Find largest blob in labeled mask
    largest_label = 0
    largest_area = 0
    for region in regionprops(label_mask):
        # take regions with large enough areas
        if region.area > largest_area:
            largest_label = region.label
            largest_area = region.area

    # Keep only largest label, discard others
    label_mask[label_mask != largest_label] = 0
    label_mask[label_mask == largest_label] = 1

    # Fill in
    label_mask = binary_fill_holes(label_mask)
    
    if name == "bg":
        label_mask = binary_erosion(label_mask, selem=selem.disk(11))
        label_mask = binary_dilation(label_mask, selem=selem.disk(15))
    
    return label_mask

def generate_colors(n=6):
    ret = []
    for i in range(n):
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        ret.append((r,g,b)) 
    return ret

# Testing
# for rgb in generate_colors():
#    print(rgb)


def generate_image_table(im_dir, num_rows=5, num_cols=3, prefixes=['original', 'label', 'gen']):
    assert(exists(im_dir))
    list_im = listdir(im_dir)

    original_i, label_i, gen_i = 1, 2, 3
    for cnt, im_name in enumerate(list_im):
        im = io.imread(join(im_dir, im_name))
        pre_found = im_name[:im_name.find('_')]
        assert(pre_found in prefixes)
        
        if (cnt) % 3 == 0:
            plt.figure(figsize=(25, 5))
        
        if pre_found == 'original':
            spec = int('13' + str(original_i))
            plt.subplot(spec)
            original_i = 1
        elif pre_found == 'label':
            spec = int('13' + str(label_i))
            plt.subplot(spec)
            label_i = 2
        elif pre_found == 'gen':
            spec = int('13' + str(gen_i))
            plt.subplot(spec)
            gen_i = 3

        plt.imshow(im)
        plt.axis('off')

        if (cnt) % 3 == 0:
            plt.tight_layout()
            plt.show()

def seg_to_rgb(seg_all):
    rgb = np.zeros((seg_all.shape[0], seg_all.shape[1], 3))
    
    for key, label in motif_labels.items():
        rgb[seg_all == label, 0] = motif_colors[key][0] / 255.0
        rgb[seg_all == label, 1] = motif_colors[key][1] / 255.0
        rgb[seg_all == label, 2] = motif_colors[key][2] / 255.0
    
    return rgb    

def list_to_txt(my_list, fname):
    with open(fname, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
            
def make_path_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

        #motif = 's'
needs_fix = ['BEN01_1', 'BEN01_2', 'BEN05', 'BM04', 'BM29', 'BM36_2', 'BM47', 'FMC16', 'GMBC02', 'GMBC13', 
             'GMBC17', 'GULB14_1', 'GULB19_2', 'GULB19_3', 'HAM07', 'IPOT27', 'KOC69', 'KOC70', 'VA53',
             'VA59_2', 'VA64']


OPERATION_DICT = {}
for name in needs_fix: OPERATION_DICT[name] = {'operation':'erosion_first', 'selem':(1,1)}

OPERATION_DICT['BEN01_1']['operation'] = 'erosion_first'
OPERATION_DICT['BEN01_1']['selem'] = (1,1)

OPERATION_DICT['BEN01_2']['operation'] = 'erosion_first'
OPERATION_DICT['BEN01_2']['selem'] = (2,2)

OPERATION_DICT['BEN05']['operation'] = 'dilation_first'
OPERATION_DICT['BEN05']['selem'] = (3,2)

OPERATION_DICT['BM04']['operation'] = 'dilation_first'
OPERATION_DICT['BM04']['selem'] = (3,4)

OPERATION_DICT['BM29']['operation'] = 'erosion_first'
OPERATION_DICT['BM29']['selem'] = (1,2)

OPERATION_DICT['BM36_2']['operation'] = 'erosion_first'
OPERATION_DICT['BM36_2']['selem'] = (2,2)

OPERATION_DICT['BM47']['operation'] = 'erosion_first'
OPERATION_DICT['BM47']['selem'] = (2,2)

OPERATION_DICT['FMC16']['operation'] = 'erosion_first'
OPERATION_DICT['FMC16']['selem'] = (2,2)

OPERATION_DICT['GMBC02']['operation'] = 'erosion_first'
OPERATION_DICT['GMBC02']['selem'] = (2,3)

OPERATION_DICT['GMBC13']['operation'] = 'erosion_first'
OPERATION_DICT['GMBC13']['selem'] = (3,4)

OPERATION_DICT['GMBC17']['operation'] = 'erosion_first'
OPERATION_DICT['GMBC17']['selem'] = (2,2)

OPERATION_DICT['GULB14_1']['operation'] = 'erosion_first'
OPERATION_DICT['GULB14_1']['selem'] = (2,2)

OPERATION_DICT['GULB19_2']['operation'] = 'erosion_first'
OPERATION_DICT['GULB19_2']['selem'] = (2,2)

OPERATION_DICT['GULB19_3']['operation'] = 'erosion_first'
OPERATION_DICT['GULB19_3']['selem'] = (3,3)

OPERATION_DICT['HAM07']['operation'] = 'erosion_first'
OPERATION_DICT['HAM07']['selem'] = (2,2)

OPERATION_DICT['IPOT27']['operation'] = 'erosion_first'
OPERATION_DICT['IPOT27']['selem'] = (2,2)

OPERATION_DICT['KOC69']['operation'] = 'erosion_first'
OPERATION_DICT['KOC69']['selem'] = (2,2)

OPERATION_DICT['KOC70']['operation'] = 'erosion_first'
OPERATION_DICT['KOC70']['selem'] = (2,2)

OPERATION_DICT['VA53']['operation'] = 'dilation_first'
OPERATION_DICT['VA53']['selem'] = (3,2)

OPERATION_DICT['VA59_2']['operation'] = 'erosion_first'
OPERATION_DICT['VA59_2']['selem'] = (2,2)

OPERATION_DICT['VA64']['operation'] = 'erosion_first'
OPERATION_DICT['VA64']['selem'] = (1,1)

#if motif == 'c':
new_fix = ['FMC18', 'LACMA06_0', 'LACMA06_2', 'MET24']
for name in new_fix: OPERATION_DICT[name] = {'operation':'erosion_first', 'selem':(1,1)}
needs_fix += new_fix
OPERATION_DICT['FMC18']['operation'] = 'erosion_first'
OPERATION_DICT['FMC18']['selem'] = (2,2)

OPERATION_DICT['LACMA06_0']['operation'] = 'erosion_first'
OPERATION_DICT['LACMA06_0']['selem'] = (2,2)

OPERATION_DICT['LACMA06_2']['operation'] = 'erosion_first'
OPERATION_DICT['LACMA06_2']['selem'] = (2,2)

OPERATION_DICT['MET24']['operation'] = 'erosion_first'
OPERATION_DICT['MET24']['selem'] = (1,1)
    
#if motif == 's':
new_fix = ['AM03', 'BM05', 'GMBC21', 'GULB14_2','LACMA04', 'NMS03', 'VA51']
for name in new_fix: OPERATION_DICT[name] = {'operation':'erosion_first', 'selem':(1,1)}
needs_fix += new_fix
OPERATION_DICT['AM03']['operation'] = 'erosion_first'
OPERATION_DICT['AM03']['selem'] = (3,3)

OPERATION_DICT['BM05']['operation'] = 'erosion_first'
OPERATION_DICT['BM05']['selem'] = (3,3)

OPERATION_DICT['GMBC21']['operation'] = 'erosion_first'
OPERATION_DICT['GMBC21']['selem'] = (3,3)

OPERATION_DICT['GULB14_2']['operation'] = 'erosion_first'
OPERATION_DICT['GULB14_2']['selem'] = (3,3)

OPERATION_DICT['LACMA04']['operation'] = 'erosion_first'
OPERATION_DICT['LACMA04']['selem'] = (2,2)

OPERATION_DICT['NMS03']['operation'] = 'erosion_first'
OPERATION_DICT['NMS03']['selem'] = (2,2)

OPERATION_DICT['VA51']['operation'] = 'dilation_first'
OPERATION_DICT['VA51']['selem'] = (2,2)


new_fix = ['BM35', 'BM16', 'BM60', 'BM61_1', 'IPOT18', 'VA52']
for name in new_fix: OPERATION_DICT[name] = {'operation':'erosion_first', 'selem':(1,1)}
needs_fix += new_fix
OPERATION_DICT['BM16']['operation'] = 'dilation_first'
OPERATION_DICT['BM16']['selem'] = (2,2)

OPERATION_DICT['BM16']['operation'] = 'erosion_first'
OPERATION_DICT['BM16']['selem'] = (2,2)

OPERATION_DICT['BM60']['operation'] = 'dilation_first'
OPERATION_DICT['BM60']['selem'] = (2,2)

OPERATION_DICT['BM61_1']['operation'] = 'erosion_first'
OPERATION_DICT['BM61_1']['selem'] = (2,2)

OPERATION_DICT['IPOT18']['operation'] = 'erosion_first'
OPERATION_DICT['IPOT18']['selem'] = (2,2)

OPERATION_DICT['VA52']['operation'] = 'erosion_first'
OPERATION_DICT['VA52']['selem'] = (2,2)

SCALAR = 1024

boundary = True

sheet_names = ['Data']

exlude_from_list = ["GULB15_0", "GULB15_1", 'BM53'] #['BM20', 'BM53']

motif_names = {'t': 'tulip', 'c': 'carnation', 's': 'saz'}

motif_labels = {'s': 1, 't': 2, 'c': 3, 'b': 4}

inverse_motif_labels = {1: 's', 2: 't', 3: 'c', 'b': 4}

motif_colors = {'t': [128, 0, 0], 'c': [0, 128, 0], 's': [0, 0, 128], 'b': [128,128,128]}

# Paths and parameters
columns_to_drop = ['id',
                   'ceramic_type',
                   'units', 
                   'where_made', 
                   'manufacturer_artist', 
                   'date_earliest',
                   'date_latest',
                   'museum_no',
                   'where_held',
                   'source', 
                   'page',
                   'use',
                   'comments',
                   'segmented']
# data_dir = '/home/salim/Documents/playground/iznik/project-iznik/data/'
data_dir = ''
version = '10-06-20'
dataset_dir = join(data_dir, 'dataset/test')
out_dir = join(data_dir, 'segmentation_' + version)
roster_name = 'Iznik_9.0_Iznik_segmented_only.csv'
chop_name = 'imagestochop.csv'
# print(join(data_dir, roster_name))
# print(exists("../../../badtest/Iznik_9.0_Iznik_segmented_only.csv"))
# Read roster
roster = read_csv_roster(join(data_dir, roster_name), columns_to_drop)

# Read chopper
chopper = np.array(read_csv_roster(join(data_dir, chop_name))).flatten().tolist()
# Read all ids
all_image_ids = roster['image_number'].as_matrix().astype('str').tolist()

# Get tulips
roster_tulip = get_only_given_motifs(roster.copy(), ['tulip_present']) # use copy to not overwrite original roster

# Get carnations
roster_carnation = get_only_given_motifs(roster.copy(), ['carnation_present']) # use copy to not overwrite original roster

# Get saz
roster_saz = get_only_given_motifs(roster.copy(), ['saz_present']) # use copy to not overwrite original roster

# Read images in dataset
image_ids_from_dataset = read_dirs(dataset_dir)
 
# Get valid images
valid_ids, invalid_ids = get_valid_images(all_image_ids, image_ids_from_dataset, [])
# Chop images based on size
chopped_dir = join(data_dir, 'chopped')
make_path_exists(chopped_dir)
valid_ids_with_chopped = valid_ids.copy()
failed_images = []
for i, name in enumerate(image_ids_from_dataset):
    motif_counters = [{"t":0, "s":0, "c":0},
                      {"t":0, "s":0, "c":0},
                      {"t":0, "s":0, "c":0},
                      {"t":0, "s":0, "c":0}]
    if name in chopper:
        exlude_from_list.append(name)
        print(i, name, 'will be chopped into 4 sub-images')
        image_dir = join(dataset_dir, name)
        
        only_files = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
        
        for file_name in only_files:
            post = file_name.split(name)[-1]
            name_no_extension = file_name.split(".")[0]
            extension = file_name.split(".")[-1]
            try:
                image, valid_name = attempt_read_image(name_no_extension, image_dir)
            except IOError:
                failed_images.append(name)
                print('read original image failed for {}, continuing...'.format(file_name))
                continue

            try:
                h, w, d = image.shape
            except ValueError:
                failed_images.append(name)
                print('gray image found {}, continuing...'.format(file_name))
                continue
                
            
            for i in range(4):
                
                chopped_dir_im = join(chopped_dir, name + "_" + str(i))
                if not name + "_" + str(i) in valid_ids_with_chopped:
                    valid_ids_with_chopped.append(name + "_" + str(i))
                make_path_exists(chopped_dir_im)
                
                # chop image here
                if i == 0:
                    image_chopped = image[:int(h/2), :int(w/2), :]
                elif i == 1:
                    image_chopped = image[:int(h/2), int(w/2)+1:, :]
                elif i == 2:
                    image_chopped = image[int(h/2)+1:, :int(w/2), :]
                elif i == 3: 
                    image_chopped = image[int(h/2)+1:, int(w/2)+1:, :]
                
                motif = name_no_extension[-1]
                if motif in motif_counters[i].keys():
                    if len(np.unique(image_chopped)) == 1:
                        continue
                    number = "{:04d}".format(motif_counters[i][motif])
                    motif_counters[i][motif] += 1
                    final_name = name + "_" + str(i) + "_" + number + "_" + motif + "." + extension
                else:
                    final_name = name + "_" + str(i) + post
                io.imsave(join(chopped_dir_im, final_name), img_as_uint(image_chopped))

# Run this for all motifs
# Read images and prepare csv
df = pd.DataFrame(columns=['ID', 'Name', 'Image Path', 'Seg Path', 'Mask Path', 'Shape', '#Tulip', '#Carnation', '#Saz'])

no_bg = []
failed_seg_images = []
failed_images = []
total_motif_cnt = 0
im_cnt = 1
motif_cnt = {'s': 0, 't': 0, 'c': 0}
for i, name in enumerate(valid_ids_with_chopped):            
    if name in exlude_from_list:
        failed_images.append(name)
        continue
    
#     if name != "VA58":
#         continue
    print(i, name)
    try:
        image, valid_name = read_original_image(name, dataset_dir)
    except IOError:
        failed_images.append(name)
        print('read original image failed, continuing...')
        continue
        
    try:
        # Reshape image if too big # this should be done before
        if image.shape[0] > SCALAR:
            image = np.round(
                rescale(image, SCALAR / (image.shape[0] * 1.0), preserve_range=True, multichannel=True)
        ).astype('uint8')
        elif image.shape[1] > SCALAR:
            image = np.round(
                rescale(image, SCALAR / (image.shape[1] * 1.0), preserve_range=True, multichannel=True)
        ).astype('uint8')
    except IndexError:
        failed_images.append(name)
        print('image needs to be resized, continuing...')
        continue
        
    # Fixing size of all smalls to 512x512
    if image.shape[0] < (SCALAR / 2) and image.shape[1] < SCALAR / 2:
        image = np.round(rescale(
            image, (SCALAR / 2) / (image.shape[0] * 1.0), preserve_range=True, multichannel=True)
        ).astype('uint8')

            
    try:
        h, w, d = image.shape
    except ValueError:
        failed_images.append(name)
        continue
        
    print('-- ', im_cnt, name, (h, w, d), total_motif_cnt)
    # Collate mask
    cnt = 0 # number of unique motifs
    seg_all = np.zeros((h, w), dtype = 'int')
    boun_all = np.zeros((h, w), dtype = 'int')
    
    # Get seg files
    seg_dir_im = join(dataset_dir, name)
    assert(exists(seg_dir_im))

    onlyfiles = [f for f in listdir(seg_dir_im) if isfile(join(seg_dir_im, f))]
    for motif in motif_cnt.keys():
        labeled_mask = np.zeros((h, w), dtype = 'int')
        for seg_file in onlyfiles:
            if seg_file.startswith(name) and '_' + motif + '.' in seg_file:  
                # Read segmentation
                seg = io.imread(join(seg_dir_im, seg_file))
                
                # Generate mask
                mask = seg[:,:,0] < 250
                
                if len(mask[mask==True]) < 50:
                    # no motif detected, skipping
                    failed_seg_images.append(seg_file)
                    print('no motif detected, skipping...')
                    continue
                    
                motif_cnt[motif] += 1
                mask = 200 * mask
                if mask.shape[0] > SCALAR:
                    mask = np.round(rescale(mask, SCALAR / (mask.shape[0] * 1.0), 
                                            preserve_range=True)).astype('uint8')
                elif mask.shape[1] > SCALAR:
                    mask = np.round(rescale(mask, SCALAR / (mask.shape[1] * 1.0), 
                                            preserve_range=True)).astype('uint8')
                # Fixing size of all smalls to 512x512
                if mask.shape[0] < (SCALAR/2) and mask.shape[1] < SCALAR/2:
                    mask = np.round(rescale(mask, SCALAR/2 / (mask.shape[0] * 1.0), 
                                            preserve_range=True)).astype('uint8')
                # Process mask
                try:
                    mask = postprocess_mask(mask, name)
                    
                    labeled_mask[mask == 1] = motif_cnt[motif]  
                except IndexError:
                    if name not in failed_images:
                        failed_images.append(name)
                        print('index error, continuing...')
                    continue
                                
        if motif_cnt[motif] > 0:
            total_motif_cnt += motif_cnt[motif]  

            # Find boundaries
            boun = find_boundaries(labeled_mask)
            boun_all += boun

            # Add mask to segmentation
            seg_all[labeled_mask > 0] = motif_labels[motif]  
            
            # Add boundary as an extra class
            if boundary:
                seg_all[boun_all > 0] = motif_labels["b"] 
                
    # BACKGROUND            
    for bg_file in onlyfiles:
        if bg_file.startswith(name) and '_a.' in bg_file: 
            # Read segmentation
            bg = io.imread(join(seg_dir_im, bg_file))
                
            # Generate mask
            maskR = bg[:,:,0] < 250 
            maskG = bg[:,:,1] < 250 
            maskB = bg[:,:,2] < 250 
            mask = np.logical_or(maskB, np.logical_or(maskR, maskG))
            
            if mask.shape[0] > SCALAR:
                mask = np.round(rescale(mask, SCALAR / (mask.shape[0] * 1.0), 
                                            preserve_range=True)).astype('uint8')
            elif mask.shape[1] > SCALAR:
                mask = np.round(rescale(mask, SCALAR / (mask.shape[1] * 1.0), 
                                            preserve_range=True)).astype('uint8')
                
            # Fixing size of all smalls to 512x512
            if mask.shape[0] < (SCALAR/2) and mask.shape[1] < SCALAR/2:
                mask = np.round(rescale(mask, SCALAR/2 / (mask.shape[0] * 1.0), 
                                        preserve_range=True)).astype('uint8')
                
            # Process mask
            try:
                bg_mask = postprocess_mask(mask, "bg").astype('uint8')  
            except IndexError:
                if name not in failed_images:
                    failed_images.append(name)
                    print('bg error, continuing...')
                continue                
        else:
            no_bg.append(name)
            
                
    if sum([val for val in motif_cnt.values()]) > 0:
        # Superimposed image
        superimposed = superimpose_image(image, boun_all)
        # mkdir out_dir in not exists 
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        
        # Save all
        imposed_dir = join(out_dir, 'imposed')
        images_dir = join(out_dir, 'images')
        segs_dir = join(out_dir, 'segs')
        pre_encoded_segs_dir = join(segs_dir, 'pre_encoded')
        masks_dir = join(out_dir, 'masks')
        bgs_dir = join(out_dir, "backgrounds")
        
        # mkdir
        if not os.path.exists(imposed_dir):
            os.mkdir(imposed_dir)
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)
        if not os.path.exists(segs_dir):
            os.mkdir(segs_dir)
        if not os.path.exists(masks_dir):
            os.mkdir(masks_dir)
        if not os.path.exists(pre_encoded_segs_dir):
            os.mkdir(pre_encoded_segs_dir)
        if not os.path.exists(bgs_dir):
            os.mkdir(bgs_dir)
                 
        superim_path = join(imposed_dir, name + '.png')
        io.imsave(superim_path, img_as_uint(superimposed).astype("uint8")) 
        im_path = join(images_dir, name + '.jpg')
        io.imsave(im_path, img_as_uint(image).astype("uint8")) 
        seg_path = join(segs_dir, name + '.png')
        io.imsave(seg_path, img_as_uint(seg_to_rgb(seg_all)).astype("uint8"))
        pre_encoded_seg_path = join(pre_encoded_segs_dir, name + '.png')
        io.imsave(pre_encoded_seg_path, img_as_uint(seg_all).astype("uint8"))
        
        gif_path = join(masks_dir, name + '.png')
        io.imsave(gif_path, img_as_ubyte(seg_all>0))
        bg_path = join(bgs_dir, name + '.png')
        io.imsave(bg_path, img_as_ubyte(bg_mask>0))

        # add to df
        df = df.append(pd.DataFrame([[im_cnt, name, im_path, seg_path, gif_path, (h, w, d), 
                                      motif_cnt['t'], motif_cnt['c'], motif_cnt['s']]], 
                                    columns=df.columns), ignore_index=True)

        # Increment im_cnt
        im_cnt += 1
    else:
        failed_images.append(name)
        
    motif_cnt = {'s': 0, 't': 0, 'c': 0}

df.to_csv(join(data_dir, 'dataset_all_' + version + '.csv'))

# Paths and parameters for motif generation
out_dir = join(data_dir, 'motifs_' + version)

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

num_out_dir = join(out_dir, 'numbered')
if not os.path.exists(num_out_dir):
    os.mkdir(num_out_dir)  
    
# Use either valid_ids or valid_ids_with_chopped
valid_ids = valid_ids_with_chopped.copy()

attributes = ['ID', 'name', 'seg_name', 'tulip', 'carnation', 'saz', "background"]
props = ['area',
         'bbox',
         'bbox_area',
         'centroid',
         'convex_area',
         'eccentricity',
         'equivalent_diameter',
         'euler_number',
         'extent',
         'inertia_tensor',
         'inertia_tensor_eigvals',
         'label',
         'local_centroid',
         'major_axis_length',
         'minor_axis_length',
         'moments',
         'moments_central',
         'moments_hu',
         'moments_normalized',
         'orientation',
         'perimeter',
         'solidity',
        ]

props_intensity = [
        "max_intensity",  
        "mean_intensity", 
        "min_intensity",  
        "weighted_centroid", 
        "weighted_local_centroid",  
        "weighted_moments",  
        "weighted_moments_central",  
        "weighted_moments_hu",  
        "weighted_moments_normalized",  
        ]
bin_size = 32
channels = ['r', 'g', 'b']
props_all = props.copy()
for channel in channels:
    for prop in props_intensity:
        props_all.append(''.join([prop, '_', channel]))
    for i in range(bin_size):
        props_all.append("".join(["hist", str(bin_size), "_", str(i), "_", channel]))


to_be_saved = ['convex_image','image']


# Run this for all motifs
font_path = "AbyssinicaSIL-R.ttf"
m_cnt = 0
df = pd.DataFrame(columns=attributes+props_all)
channels = {0: 'r', 1: 'g', 2: 'b'}
failed_images = []
total_motif_cnt = 0
motif_cnt = {'s': 0, 't': 0, 'c': 0, 'a': 0}
print(valid_ids)
for i, name in enumerate(valid_ids):
#     print("working on "+name)
    if name in exlude_from_list:
        continue
#     if name != "AM02":
#         continue
#     if i == 4:
#         break
    
    try:
        image, valid_name = read_original_image(name, dataset_dir)
#         print("loaded "+valid_name)
#         print(image[:,:,2])
    except IOError:
        failed_images.append(name)
        print('read original image failed, continuing...')
        continue
        
    try:
        # Reshape image if too big # this should be done before
        if image.shape[0] > SCALAR:
            image = np.round(
                rescale(image, SCALAR / (image.shape[0] * 1.0), preserve_range=True, multichannel=True)
        ).astype('uint8')
        elif image.shape[1] > SCALAR:
            image = np.round(
                rescale(image, SCALAR / (image.shape[1] * 1.0), preserve_range=True, multichannel=True)
        ).astype('uint8')
    except IndexError:
        failed_images.append(name)
        print('image needs to be resized, continuing...')
        continue
        
           
    # Fixing size of all smalls to 512x512
    if image.shape[0] < (SCALAR/2) and image.shape[1] < SCALAR/2:
#         print("fixed size")
        image = np.round(rescale(image, (SCALAR/2) / (image.shape[0] * 1.0), preserve_range=True)).astype('uint8')
            
    try:
        h, w, d = image.shape
#         print("assigned hwd")
#         print(h,w,d)
    except ValueError:
        continue
        failed_images.append(name)

    index = 0 # index for saving to df
    print('-- ', name, (h, w), total_motif_cnt)

    # Collate mask
    cnt = 0 # number of unique motifs
    seg_all = np.zeros((h, w), dtype = 'int')
    boun_all = np.zeros((h, w), dtype = 'int')
    
    # Get seg files
    seg_dir_im = join(dataset_dir, name)
    assert(exists(seg_dir_im))
    
    onlyfiles = [f for f in listdir(seg_dir_im) if isfile(join(seg_dir_im, f))]
#     print(onlyfiles)
#     print("onlyfiles")
    all_motifs_labeled_mask = np.zeros((h, w), dtype = 'int')
    
    seg_names = {'s': [], 't': [], 'c': [], 'a':[]}
    latest_indices = []
    for motif in motif_cnt.keys():
#         print(image[:,:,2])
#         print("on "+motif)
        labeled_mask = np.zeros((h, w), dtype = 'int')
        for seg_file in onlyfiles:
#             print("   on "+seg_file)
            if seg_file.startswith(name) and '_' + motif + '.' in seg_file:
#                 print(motif+ "  found and working")
                motif_cnt[motif] += 1
#                 print(str(motif_cnt[motif])+ " updated ")
                # Read segmentation
                seg = io.imread(join(seg_dir_im, seg_file))
                
                # Generate mask
                mask = seg[:,:,0] < 250
                mask = 200 * mask
                # Handle BG
                if motif == "a":
                    # Generate mask
                    maskR = seg[:,:,0] < 250 
                    maskG = seg[:,:,1] < 250 
                    maskB = seg[:,:,2] < 250 
                    mask = np.logical_or(maskB, np.logical_or(maskR, maskG))
            
                if mask.shape[0] > SCALAR:
                    mask = np.round(rescale(mask, SCALAR / (mask.shape[0] * 1.0), 
                                            preserve_range=True)).astype('uint8')
                elif mask.shape[1] > SCALAR:
                    mask = np.round(rescale(mask, SCALAR / (mask.shape[1] * 1.0), 
                                            preserve_range=True)).astype('uint8')

                # Fixing size of all smalls to 512x512
                if mask.shape[0] < (SCALAR/2) and mask.shape[1] < SCALAR/2:
                    mask = np.round(rescale(mask, SCALAR/2 / (mask.shape[0] * 1.0), 
                                            preserve_range=True)).astype('uint8')

                # Process mask
                try:
                    if motif == "bg":
                        mask = postprocess_mask(mask, "bg") if motif == "bg" else postprocess_mask(mask, name)
                    else:
                        mask = postprocess_mask(mask, name)
                        labeled_mask[mask == 1] = motif_cnt[motif]  
                    seg_names[motif].append(seg_file.split('.')[0])
                except IndexError:
                    if name not in failed_images:
                        failed_images.append(name)
                        print('index error, continuing...')
                    continue
 
        if motif_cnt[motif] > 0:
            print("more than one, and working on " + motif)
            # Keep track of all motifs
            ################################################
            max_label = all_motifs_labeled_mask.flatten().max()
            for ii in range(1, labeled_mask.flatten().max() + 1):
                all_motifs_labeled_mask[labeled_mask == ii] = max_label + ii
            ################################################
            
            # Compute and save region props
            masks = []
            for key, val in channels.items():
#                 print("channels.items")
#                 print(key, val)
                regions = regionprops(labeled_mask, intensity_image=image[:,:,key])
                for j, region in enumerate(regions):
                    if key == 0:
                        latest_indices.append(j+m_cnt)
                        meta = [''.join([name, '_', str(j+index)]), name, seg_names[motif][j], int(motif == 't'), int(motif == 'c'), int(motif == 's'), int(motif == 'a')]
                        print(meta, j+m_cnt, j+index)
                        features = []
                        for a in props:
                            #print(a, getattr(region, a))
                            features.append(getattr(region, a))

                        for a in to_be_saved:
                            mask = getattr(region, a)
                            a = a.replace("image", "mask")
                            superim_path = join(out_dir, ''.join([name, '_', str(j+index), '_', a, '.png']))
                            io.imsave(superim_path, img_as_uint(mask)) 
                        
                        masks.append(mask)
                        
                        dummy_list = [0] * (len(df.columns) - len(meta) - len(features))
                        
                        df = df.append(
                            pd.DataFrame([meta+features+dummy_list], columns=df.columns
                                      ), ignore_index=True)
                        
                    features_intensity = []
                    for a in props_intensity:
                        #print(a, getattr(region, a))
                        features_intensity.append(getattr(region, a))
                        df["".join([a, "_", val])][j+m_cnt] = features_intensity[-1]
                        
                    x = getattr(region, 'intensity_image')
                    superim_path = join(out_dir, ''.join([name, '_', str(j+index), '_intensity_image_', val, '.png']))
                    io.imsave(superim_path, img_as_uint(x)) 

                    masked = x[masks[j] > 0]
                    n, bins = np.histogram(masked, density=True, range=(0, 256), bins=bin_size)
                    hists = list(n)
                      
                    #print(hists)
                    for ii, bin_h in enumerate(hists):
                        df["".join(["hist", str(bin_size), "_", str(ii), "_", val])][j+m_cnt] = bin_h

            m_cnt += motif_cnt[motif]
            index += motif_cnt[motif]
    
    #######################################
    source_img = Image.fromarray((all_motifs_labeled_mask > 0).astype(np.uint8) * 255).convert("RGBA")
    font = ImageFont.truetype(font_path, int(all_motifs_labeled_mask.shape[0]/40))
    try:
        assert(len(latest_indices) == all_motifs_labeled_mask.flatten().max())
    except AssertionError:
        continue
    for ii in range(all_motifs_labeled_mask.flatten().max()):
        draw = ImageDraw.Draw(source_img)
        try:
            draw.text((df["weighted_centroid_b"][latest_indices[ii]][1], 
                   df["weighted_centroid_b"][latest_indices[ii]][0]), 
                   str(ii), fill=(0,0,0), font=font)
        except TypeError:
            continue
    source_img_path = join(num_out_dir, name)
    source_img.save(source_img_path, "PNG")    
    #######################################
    
    #break
                
    motif_cnt = {'s': 0, 't': 0, 'c': 0, 'a': 0}

df.to_csv(join(data_dir, 'motif_props_all_' + version + '_with_bg.csv'))
