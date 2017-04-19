# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import db
import matplotlib.dates as mdates
from datetime import datetime, timedelta
#import statsmodels.api as sm


from pony.orm import *
db = Database()
db.bind('mysql', host='', user='opit', passwd='332', db='marimba')
db.generate_mapping(create_tables=True)

def window(size):
    return np.ones(size)/float(size)
    

time_slice_start = '2017-03-02 16:00:00'
time_slice_end = '2017-03-02 16:00:30'


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
	return db.select("select time_finish from data")

@db_session
def get_mb_in_region(region):
	return db.select("select mb from data where time_start > $time_slice_start and time_start < $time_slice_end and cell_grp = $region")

@db_session
def get_time_start_in_region(region):
	return db.select("select time_start from data where time_start > $time_slice_start and time_start < $time_slice_end and cell_grp = $region")


plt.figure()


for region in [1, 2, 3, 4]:
	mb = get_mb_in_region(region)
	session_start = get_time_start_in_region(region)
	ax = plt.subplot(2, 2, region)
	avg = np.convolve(mb,window(100), 'same')
	ax.plot_date(session_start, mb, c='k', markersize=1)
	ax.plot(session_start, avg, c='r', linestyle='-', markersize=1)
	#plt.date_plot(districts, mb)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%S'))
	ax.set_yscale('log')
plt.ylabel("MB, vidurkis")
plt.savefig("img/session_avg_30sec_in_regions", bbox_inches="tight")




#@db_session
#def get_mb():
#	return db.select("select id from cells")[:10]
	
mb = get_mb()
session_start = get_time_start()
districts = get_districts()
#session_end = get_time_end()

#apie 4% mb = 0 

exit()
    
avg = np.convolve(mb,window(100), 'same')
    
plt.figure()
ax = plt.subplot()
plt.plot_date(session_start, mb, c='k', markersize=1)
plt.plot(session_start, avg, c='r', linestyle='-', markersize=1)
#plt.date_plot(districts, mb)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set_yscale('log')
plt.ylabel("MB, vidurkis")
plt.savefig("img/session_avg_30sec", bbox_inches="tight")


plt.figure()
ax = plt.subplot()
plt.hist(session_start, facecolor="Salmon", bins=20)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#plt.xlabel("%H:%M")
plt.ylabel("Sesiju sk.")
plt.savefig("img/session_time_hist", bbox_inches="tight")


plt.figure()
ax = plt.subplot()
plt.plot_date(session_start, mb, c='k', markersize=1)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H'))
plt.ylabel("MB")
plt.xlabel("")
ax.set_yscale('log')
plt.savefig("img/session_time_30s.png", bbox_inches="tight")



'''
plt.figure()
ax = plt.subplot()
plt.plot_date(session_start, mb, c='k', markersize=1)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
plt.ylabel("MB")
plt.xlabel("Valanda")
ax.set_yscale('log')
plt.savefig("img/session_time_20min.png", bbox_inches="tight")



fig = plt.figure()
for region in range(1, 5):
	ax = subplots(1,4,i)
	ax.hist(session_start[np.where(aps==i)], color='lightblue', bins=8)
	plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%m'))
#ax.xaxis.set_major_locator(mdates.YearLocator())
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
plt.savefig("img/session_hist_regions")
plt.close()



fig, ax = plt.subplots(1,1)
ax.hist(session_start, color='lightblue', bins=8)
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%m'))
#ax.xaxis.set_major_locator(mdates.YearLocator())
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
plt.savefig("img/session_hist")
plt.close()



print len(mb), np.mean(mb), np.std(mb), np.max(mb), np.median(mb)
n, bins, patches = plt.hist(mb, bins=100, log=True, facecolor="red")
plt.axis([0, np.max(mb), 0, np.max(n)])
plt.xlabel("Sesija, MB")
plt.ylabel("N")
plt.savefig("img/mbs_hist")
plt.close()

mb = mb[np.where(mb < 1)]
print len(mb), np.mean(mb), np.std(mb), np.max(mb), np.median(mb)

n, bins, patches = plt.hist(mb, bins=100, log=True, facecolor="red")
plt.axis([0, np.max(mb), 0, np.max(n)])
plt.xlabel("Sesija, MB")
plt.ylabel("N")
plt.savefig("img/mbs_hist_fine")
plt.close()


n, bins, patches = plt.hist(aps, bins=4, log=False, facecolor="royalBlue")
ax = plt.gca()
#ax.set_xticks("", "Vno/Utena", "Kns/Mar/Aly", "Klp/Tel/Taur", "Siaul/Pnv")
#ax.set_xticklabels(["Vno/Utena", "Kns/Mar/Aly", "Klp/Tel/Taur", "Siaul/Pnv"])
plt.xlabel("Prisijungimai regionuose")
plt.ylabel("N")
plt.savefig("img/regions_hist")
'''
