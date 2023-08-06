import numpy as np
from numpy import pi,sqrt
from .constants import Earth

# Add some SMAD calculations here

def period(a):
    # a [km] -> period [sec]
    return 2*pi*sqrt(a**3/Earth.mu)

def dnode(period):
    """
    Orbit nodal precession on each rev. Orbits below GEO move (drift) Westerly
    while orbits above GEO move Easterly. Orbits at GEO are stationary, 0 deg drift.
    Use siderial day rotation for better accuracy.

    Arg:
    period [sec]
    Return:
    node precession (dn) [deg]
    """
    return 360 - 360/(23*3600+56*60+4)*period
