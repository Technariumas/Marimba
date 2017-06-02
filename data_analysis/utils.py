
import numpy as np
from datetime import datetime, timedelta
from pony.orm import *

from marimba_config import *

data_table = 'data_0526'

db = Database()
db.bind('mysql', host='', user='opit', passwd='332', db='data')
db.generate_mapping(create_tables=True)


def make_threshold(array, note):
	print note, "note", array.shape
	if note == 0:
		lowest = np.percentile(array, 50)
		lower = np.percentile(array, 67)
		upper = np.percentile(array, 83)
	else:
		lowest = np.percentile(array, 40)
		lower = np.percentile(array, 60)
		upper = np.percentile(array, 80)
	lowest_octave = np.where(array <= lowest)
	lower_octave = np.where((array <= lower) & (array > lowest))
	upper_octave = np.where((array <= upper) & (array > lower))
	top_octave = np.where(array > upper)
	array[lowest_octave] = 3
	array[lower_octave] = 4
	array[upper_octave] = 5
	array[top_octave] = 6		
	return array

def get_duration():
	return (datetime.strptime(time_slice_end, '%Y-%m-%d %H:%M:%S') - datetime.strptime(time_slice_start, '%Y-%m-%d %H:%M:%S')).seconds

def rolling_window(a, window):
	shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
	strides = a.strides + (a.strides[-1],)
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def rolling_sum(a, n) :
	return np.convolve(a,np.ones(n),'same')

def moving_sum(a, n) :
    ret = np.sum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:]# / n

def window(size):
    return np.ones(size)/float(size)
    
@db_session
def get_list_of_districts():
	return db.select("select distinct raj from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end")

@db_session
def get_districts():
	return db.select("select raj from data_0526 where time_start>= $time_slice_start and time_start < $time_slice_end")

@db_session
def get_mb():
	return db.select("select mb from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end")

@db_session
def get_time_start():
	return db.select("select time_start from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end order by time_start")

@db_session
def get_session_count(region):
	return db.select("select count(time_start) from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end and cell_grp = $region")

@db_session
def get_unique_times_start(region):
	return db.select("select distinct time_start from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end and cell_grp = $region order by time_start")

@db_session
def get_time_end():
	return db.select("select time_finish from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end order by time_start")
 
@db_session
def get_mb_in_region(region):
	return db.select("select mb from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end and cell_grp = $region order BY time_start")

@db_session
def get_duration():
	return (datetime.strptime(time_slice_end, '%Y-%m-%d %H:%M:%S') - datetime.strptime(time_slice_start, '%Y-%m-%d %H:%M:%S')).seconds

def get_time_start_in_region(region):
	return db.select("select time_start from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end and cell_grp = $region order by time_start")

#@db_session
#def get_session_duration():
#	return db.select("select datediff(time_finish,time_start) from $data_table where time_start >= $time_slice_start and time_start < $time_slice_end")

@db_session
def mb_per_second_in_region(region):
	return db.select("sum(mb) as sum_mb from data_0526 where time_start >= $time_slice_start and time_start < $time_slice_end and cell_grp = $region GROUP BY time_start")

