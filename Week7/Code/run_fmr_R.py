#!/usr/bin/env python3
"""run r from python"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import subprocess
import ipdb

#Popen.stdout
#If the stdout argument was PIPE, this attribute is a file object that provides output from the child process. Otherwise, it is None.
#Popen.stderr
#If the stderr argument was PIPE, this attribute is a file object that provides error output from the child process. Otherwise, it is None.
p = subprocess.Popen("Rscript fmr.R", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


#Popen.communicate(input=None)
#Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate. The optional input argument should be a string to be sent to the child process, or None, if no data should be sent to the child.
#communicate() returns a tuple (stdoutdata, stderrdata).
stdout, stderr = p.communicate()

# ipdb.set_trace()
if stderr:
    print("--------------")
    print("Raise error:")
    print(stderr.decode())
else:
    print("--------------")
    print("fmr.R is executed:")
    print(stdout.decode())