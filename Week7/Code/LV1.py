#!/usr/bin/env python3
"""Lotka-Volterra Model in scipy"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import scipy as sc
import scipy.integrate as integrate
import matplotlib.pylab as p
import matplotlib.backends.backend_pdf

def dCR_dt(pops, t=0):
    """Returns the growth rate of predator and prey populations at any given time step"""

    R = pops[0]
    C = pops[1]
    dRdt = r*R - a*R*C
    dCdt = -z*C + e*a*R*C

    return sc.array([dRdt, dCdt])


# Define parameters:
# Resource growth rate
r = 1.
# Consumer search rate
a = 0.1
# Consumer mortality rate
z = 1.5
# Consumer production efficiency
e = 0.75

# integrate 0-15, 1000 points:
t = sc.linspace(0, 15, 1000)

# init: 10 prey, 5 predator
R0 = 10
C0 = 5
RC0 = sc.array([R0, C0])

pops, infodict = integrate.odeint(dCR_dt, RC0, t, full_output=True)

print(infodict['message'])



# Plot population densityb
f1 = p.figure()
p.plot(t, pops[:, 0], 'g-', label='Resource density') 
p.plot(t, pops[:, 1], 'b-', label='Consumer density')
p.grid()
p.legend(loc='best')
p.xlabel('Time')
p.ylabel('Population density')
p.title('Consumer-Resource population dynamics')
# p.show()


f2 = p.figure()
p.plot(pops[:, 0], pops[:, 1], 'r-', label='Consumer density')
p.grid()
p.xlabel('Resource density')
p.ylabel('Consumer density')
p.title('Consumer-Resource population dynamics')
# p.show()

pdf = matplotlib.backends.backend_pdf.PdfPages('../Results/LV1.pdf')
pdf.savefig(f1)
pdf.savefig(f2)
pdf.close()
p.close('all')