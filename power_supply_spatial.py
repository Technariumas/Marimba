#10 power supply segments: 1-10
#2, 3, 5 have one box missing

import numpy as np


power_supply = np.zeros((10, 8), dtype='int')
power_supply[0:2,0:4] = 1
power_supply[2:4,0:4] = 2
power_supply[4:6,0:4] = 3
power_supply[6:8,0:4] = 4
power_supply[8:,0:4] = 5
power_supply[0:2,4:] = 6
power_supply[2:4,4:] = 7
power_supply[4:6,4:] = 8
power_supply[6:8,4:] = 9
power_supply[8:,4:] = 10

def return_group_by_index(ind):
	return power_supply[ind]
	
def return_current_power_supply_group_indices(group):
	return np.where(power_supply == group)	

def get_current_segment(y, x):
	if (x >= 0 and x < 4):
		if y < 2: return 1
		elif (y > 1 and y < 4): return 2
		elif (y > 3 and y < 6): return 3
		elif (y > 5 and y < 8): return 4
		elif (y > 7 and y < 10): return 5
	elif (x > 3 and x < 8):
		if y < 2: return 6
		elif (y > 1 and y < 4): return 7
		elif (y > 3 and y < 6): return 8
		elif (y > 5 and y < 8): return 9
		elif (y > 7 and y < 10): return 10
	else: 
		print "wrong index:", y, x
		return 0

#print get_current_segment(1, 9)
#print return_group_by_index((3,4))

print power_supply
print return_current_power_supply_group_indices(1)
print power_supply[return_current_power_supply_group_indices(1)]
