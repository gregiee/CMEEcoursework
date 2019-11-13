#!/usr/bin/env python3
"""Lotka-Volterra Model in scipy take command args, with appropriate paras, and discrete, with a random gaussian fluctuation"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import sys
import scipy as sc
import scipy.stats as stats
import matplotlib.pylab as p
import matplotlib.backends.backend_pdf


def dCR_dt(RC0, t=0):
    """ Returns the growth rate of predator and prey populations at any given time step """
    # create pre-rendered with 0s
    RC = sc.zeros((t, 2))
    RC[0, 0] = RC0[0]
    RC[0, 1] = RC0[1]
    for i in range(t-1):
        # add norm fluctuation (-.1,.1) to avoid booming R 
        RC[i+1, 0] = RC[i, 0] * \
            (1 + (r + stats.norm.rvs(loc=0, scale=0.1)) *
             (1 - RC[i, 0] / K) - a * RC[i, 1])
        RC[i+1, 1] = RC[i, 1] * \
            (1 - z + stats.norm.rvs(0, 0.1) + e * a * RC[i, 0])

    return RC


# Define parameters:
if len(sys.argv) == 6:
    # Resource growth rate
    r = float(sys.argv[1])
    # Consumer search rate
    a = float(sys.argv[2])
    # Consumer mortality rate
    z = float(sys.argv[3])
    # Consumer production efficiency
    e = float(sys.argv[4])
    # Carrying capacity
    K = float(sys.argv[5])
else:
    r = 1.   
    a = 0.1
    z = 1.5
    e = 0.75
    K = 35



# define time and init R0 and C0
t = 170
R0 = 10
C0 = 5

# init: 10 prey, 5 predator
RC0 = sc.array([R0, C0], dtype='float')
RC = dCR_dt(RC0, t)
print("consumer density: %s, resource density: %s" %(RC[t-1, 1], RC[t-1, 0]))



f1 = p.figure()
p.plot(range(t), RC[:, 0], 'g-', label='Resource density')
p.plot(range(t), RC[:, 1], 'b-', label='Consumer density')
p.grid()
p.legend(loc='best')
p.xlabel('Time')
p.ylabel('Population density')
p.title('Consumer-Resource population dynamics')
# p.show()  # To display the figure

f2 = p.figure()
p.plot(RC[:, 0], RC[:, 1], 'r-', label='Consumer density')
p.grid()
p.xlabel('Resource density')
p.ylabel('Consumer density')
p.title('Consumer-Resource population dynamics')
# p.show()  # To display the figure

pdf = matplotlib.backends.backend_pdf.PdfPages('../Results/LV4.pdf')
pdf.savefig(f1)
pdf.savefig(f2)
pdf.close()
p.close('all')
