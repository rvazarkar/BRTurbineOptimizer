# This script calculates the best coil and reactor build for efficiency
# based on the steam input to the turbine as well as the material chosen
# for the coil

import math
import sys

debug = False

# These are the values assigned to different blocks in the coil. Higher
# numbers are always better (iron is awful)
data = {
    "ludicrite": [3.5, 1.02, 3.5],
    "enderium": [3, 1.02, 3],
    "iron": [1, 1, 1],
    "gold": [2, 1, 1.75],
    "fluxedelectrum": [2.5, 1.01, 2.2],
    "manyullyn": [3.5, 1, 2.5],
    "copper": [1.2, 1, 1.2],
    "osmium": [1.2, 1, 1.2],
    "zinc": [1.35, 1, 1.3],
    "lead": [1.35, 1, 1.3],
    "brass": [1.4, 1, 1.2],
    "bronze": [1.4, 1, 1.2],
    "aluminum": [1.5, 1, 1.3],
    "steel": [1.5, 1, 1, 3],
    "invar": [1.5, 1, 1.4],
    "silver": [1.7, 1, 1.5],
    "electrum": [2.5, 1, 2.0],
    "platinum": [3, 1, 2.5],
    "shiny": [3, 1, 2.5],
    "titanium": [3.1, 1, 2.7],
    "mithril": [2.2, 1, 1, 5],
    "orichalcum": [2.3, 1, 1, 7],
    "quicksilver": [2.6, 1, 1, 8],
    "haderoth": [3, 1, 2],
    "celengil": [3, 3, 1, 2.25],
    "tartarite": [3.5, 1, 2.5]
}

# The 2 most efficient RPMs are 1796 and 898 according to the efficiency
# algorithm. We target 1796 for obvious reasons. Feel free to change this
# as you see fit
target_rpm = 1796

# Max steam for a turbine is 2000 mb/t. We're not covering multiple
# turbines in this
steam = int(input("Steam (max 2000 mb/t): "))
if steam > 2000:
    print "Maximum steam input for a turbine is 2000!"
    sys.exit()
material = raw_input("Name of material (No spaces, default enderium): ")

material = material.lower()

# Enderium is more reasonable than Ludicrite as a default
if material == "":
    material = "enderium"

if not material.lower() in data:
    print "{0} not found, defaulting to enderium".format(material)
    material = "enderium"

# We cant use part of a blade, so you really want a multiple of 25 for steam
blades = math.floor(steam / 25)

lift_torque = blades * 25 * 10
induction_torque = target_rpm * (.1 * data[material][2])
blade_drag = .00025 * blades * 1
frictional_drag = ((blades * 10) + math.ceil(blades / 4)) * .01 * 1

aerodynamic_drag_torque = target_rpm * blade_drag

best = 1000
num = 1

# We want the RPMFormula to yield a number as close to 0 as possible,
# which indicates that the negative factors are almost balanced with the
# positive ones
for i in xrange(1, 1000):
    rotor_energy = lift_torque + \
        (-1 * (induction_torque * i)) + \
        (-1 * aerodynamic_drag_torque) + (-1 * frictional_drag)
    rpmformula = rotor_energy / (blades * 10)
    if abs(rpmformula) < best:
        if debug:
            print "Found new best coil at i = {0} with coefficient of {1}".format(str(i), str(rpmformula))
        best = rpmformula
        num = i

# Each coil can have 8 blocks, but you can also use partials. Add 1 to the
# length if we have a partial
coil_length = math.floor(num / 8)
if num % 8 > 0:
    coil_length += 1

induction_torque = induction_torque * num
induction_exponent = (num * data[material][1]) / num
# The weird number at the end is the best value acheived from the
# efficiency algorithm at 1796 RPM
energy = (math.pow(induction_torque, induction_exponent)
          * (.33 * data[material][0])) * 0.9999995606

bestsa = 1000000
length = 1000
width = 1000
height = 1000
rotors = 10000
blength = 100000

# Calculate the lowest surface area using different combinations of rotor
# blade lengths
for i in xrange(1, 11):
    tlength = blades / (i * 4)
    if blades % (i * 4) > 0:
        tlength += 1
    tlength = int(tlength)
    twidth = (i * 2) + 3
    theight = twidth
    total_length = tlength + coil_length + 2
    sa = 2 * ((twidth * total_length) +
              (theight * total_length) + (theight * twidth))
    if sa < bestsa and total_length <= 32:
        bestsa = sa
        width = twidth
        height = theight
        length = int(total_length)
        rotors = i
        blength = tlength

# The default length limit for turbines is 16, so if we go over that,
# we'll build up instead, where the  limit is 32
if length > 16:
    theight = height
    height = length
    length = theight

outerblocks = (length * 4 + width * 4 + height * 4) - 16

if bestsa == 1000000:
    print "--------------------------------------------------------------------------------"
    print "Unable to optimize this reactor! Your coil material is likely not efficient enough!"
    print "--------------------------------------------------------------------------------"
else:
    print "--------------------------------------------------------------------------------"
    print "Number of Blades: {0}".format(str(blades))
    print "Number of Blocks of {0}: {1} ({2} ingots)".format(material.title(), str(num), str(num * 9))
    print "Length of Coil: {0}".format(str(coil_length))
    print "Energy generated per tick: {0}".format(str(energy))
    print "Cheapest turbine setup: {0}x{1}x{2} (LxWxH) with {3} ({4} casing blocks) and a blade length of {5}".format(str(length), str(width), str(height), str(bestsa), str(outerblocks), str(rotors))
    print "Rotor Blade length is {0}".format(str(blength))
    print "--------------------------------------------------------------------------------"
