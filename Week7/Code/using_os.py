#!/usr/bin/env python3
"""os practical"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

# Use the subprocess.os module to get a list of files and  directories 
# in your ubuntu home directory 

# Hint: look in subprocess.os and/or subprocess.os.path and/or 
# subprocess.os.walk for helpful functions

import subprocess
import ipdb

#################################
#~Get a list of files and 
#~directories in your home/ that start with an uppercase 'C'

# Type your code here:

# Get the user's home directory.
home = subprocess.os.path.expanduser("~")

# Create a list to store the results.
FilesDirsStartingWithC = []

# Use a for loop to walk through the home directory.
for (dir, subdir, files) in subprocess.os.walk(home):
  for d in dir:
    # get the first letter instead of the whole name
    if d[0].startswith("C"):
      FilesDirsStartingWithC.append(d)
  for d in subdir:
    if d[0].startswith("C"):
      FilesDirsStartingWithC.append(d) 
  for f in files:  
    if f[0].startswith("C"):
      FilesDirsStartingWithC.append(f)  
  
print('Files/Directories starting with "C":')
print(set(FilesDirsStartingWithC))
#################################
# Get files and directories in your home/ that start with either an 
# upper or lower case 'C'

# Type your code here:
FilesDirsStartingWithc_C = []
for (dir, subdir, files) in subprocess.os.walk(home):
    for d in dir:
      if d[0].lower().startswith("c"):
        FilesDirsStartingWithC.append(d)
    for d in subdir:
      if d[0].lower().startswith("c"):
        FilesDirsStartingWithc_C.append(d)
    for f in files:
      if f[0].lower().startswith("c"):
        FilesDirsStartingWithc_C.append(f)

print('Files/Directories starting with "C/c":')
print(set(FilesDirsStartingWithc_C))

#################################
# Get only directories in your home/ that start with either an upper or 
#~lower case 'C' 

# Type your code here:
DirsStartingWithc_C = []
for (dir, subdir, files) in subprocess.os.walk(home):
    for d in dir:
      if d[0].lower().startswith("c"):
        DirsStartingWithc_C.append(d)
    for d in subdir:
      if d[0].lower().startswith("c"):
        DirsStartingWithc_C.append(d)

print('Directories starting with "C/c":')
print(set(DirsStartingWithc_C))