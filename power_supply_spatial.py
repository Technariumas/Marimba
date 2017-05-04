#10 power supply segments: 1-10
#2, 3, 5 have one box missing

import numpy as np

def get_power_supply_map():
	power_supply_map = np.zeros((10, 8), dtype='int')
	power_supply_map[0:2,0:4] = 1
	power_supply_map[2:4,0:4] = 2
	power_supply_map[4:6,0:4] = 3
	power_supply_map[6:8,0:4] = 4
	power_supply_map[8:,0:4] = 5
	power_supply_map[0:2,4:] = 6
	power_supply_map[2:4,4:] = 7
	power_supply_map[4:6,4:] = 8
	power_supply_map[6:8,4:] = 9
	power_supply_map[8:,4:] = 10
	return power_supply_map

def return_group_by_index(ind):
	power_supply_map = get_power_supply_map()
	return power_supply_map[ind]
	
def return_current_power_supply_group_indices(group):
	power_supply_map = get_power_supply_map()
	return np.where(power_supply_map == group)	

