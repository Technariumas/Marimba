
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pony.orm import *

from marimba_config import *
db = Database()
db.bind('mysql', host='', user='opit', passwd='332', db='marimbatest')
db.generate_mapping(create_tables=True)

durations = np.genfromtxt("../../data/duration.csv")
durations*=0.0001

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
	return db.select("select distinct raj from data where time_start > $time_slice_start and time_start < $time_slice_end")

@db_session
def get_districts():
	return db.select("select raj from data where time_start > $time_slice_start and time_start < $time_slice_end")

@db_session
def get_mb():
	return db.select("select mb from data where time_start > $time_slice_start and time_start < $time_slice_end")

@db_session
def get_time_start():
	return db.select("select time_start from data where time_start > $time_slice_start and time_start < $time_slice_end")


@db_session
def get_time_end():
	return db.select("select time_finish from data where time_start > $time_slice_start and time_start < $time_slice_end")

@db_session
def get_mb_in_region(region):
	return db.select("select mb from data where time_start > $time_slice_start and time_start < $time_slice_end and cell_grp = $region")

@db_session
def get_time_start_in_region(region):
	return db.select("select time_start from data where time_start > $time_slice_start and time_start < $time_slice_end and cell_grp = $region")

@db_session
def get_session_duration():
	return db.select("select time_finish-time_start from data where time_start > $time_slice_start and time_start < $time_slice_end")

@db_session
def mb_per_second_in_region(region):
	return db.select("sum(mb) as sum_mb from data where time_start > $time_slice_start and time_start < $time_slice_end and cell_grp = $region GROUP BY time_start")

