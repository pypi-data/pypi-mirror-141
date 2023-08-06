from collections import namedtuple
from math import pi

# value?
femto = 1E-15
pico = femto*1000
nano = pico*1000
micro = nano*1000
milli = micro*1000
centi = 1E-2
kilo = 1E3
mega = kilo*1000
giga = mega*1000

# conversions
deg2rad = pi/180
rad2deg = 180/pi

LagrangePoint = namedtuple("LagrangePoint","L1 L2 L3 L4 L5")
EarthMoonLagrange = LagrangePoint(326000e3,448900e3,381680e3,384400e3,384400e3) # m
SunEarthLagrange = LagrangePoint(148.11e9,151.1e9,149.6e9,149.6e9,149.6e9)
GEO = 42164e3 # m

speedOfLight = 3*10**8 # m/s

# FIXME: change grav const to km^3/sec^2?? orbits use km not m
# https://en.wikipedia.org/wiki/Standard_gravitational_parameter
# mu = GM
# G = standard gravitational parameter of celectial body
# M = mass of body

# radius [km]
# mass [kg]
# standard gravitational const [m^3/sec^2]
# tilt [deg]


Body = namedtuple("Body", "radius mass mu tilt geo")

to_km3 = 1/1000/1000/1000
# https://en.wikipedia.org/wiki/Earth
Earth = Body(6378.388, 5.97237E24, 3.986004418E14*to_km3, 23.4392811, 42164)

# https://en.wikipedia.org/wiki/Moon
Moon = Body(1737.4, 7.342e22, 4.9048695e12*to_km3, 1.5424, None)
