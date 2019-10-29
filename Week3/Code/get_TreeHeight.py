#!/usr/bin/env python3
"""input distance and angle to calculates heights of trees"""

__author__ = 'Yuchen Yang (yy5819@ic.ac.uk)'
__version__ = '0.0.1'

import sys
import pandas as pd
import numpy as np
import re

def loadFile(filepath):
    """Read and load file, return data"""
    data = pd.read_csv(filepath)
    return data

def TreeHeight(data):
    """input(degrees, distance), output height"""
    degrees = data['Angle.degrees']
    distance = data['Distance.m']
    radians = np.deg2rad(degrees)
    height = distance * np.tan(radians)
    data['height'] = height
    return data

def writeFile(data, filepath):
    """write file to Result folder with a name InputFileName_treeheights.csv"""
    file = re.findall(r"/+([\w\d]+).csv", filepath)
    filename = file[0] + r'_treeheights.csv'
    path = '../Results/' + filename
    data.to_csv(path, index=False)
    print("Done!")


def main(argv):
    """main function that runs the script"""
    data = loadFile(sys.argv[1])
    output = TreeHeight(data)
    writeFile(output, sys.argv[1])


if(__name__ == "__main__"):
    status = main(sys.argv)
    sys.exit("Exit")
