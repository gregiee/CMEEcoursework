#!/usr/bin/env python3
"""test runing r example"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import subprocess
subprocess.Popen("/usr/bin/Rscript --verbose TestR.R > \
../Results/TestR.Rout 2> ../Results/TestR_errFile.Rout", shell=True).wait()