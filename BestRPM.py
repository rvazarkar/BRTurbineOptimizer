# This script helps you calculate the best RPM possible based on the
# BigReactors efficiency algorithm. 896 and 1796 come back as best.
# Including this script for documentation purposes
import math

max_effic = 0
rpm = 0

for i in range(1000, 2000):
    efficiency = (.25 * math.cos(i / (45.5 * math.pi))) + .75
    if efficiency > max_effic:
        max_effic = efficiency
        rpm = i

print rpm
print max_effic
