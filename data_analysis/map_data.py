from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

from pony.orm import *
db = Database()
db.bind('mysql', host='', user='opit', passwd='332', db='marimba')
db.generate_mapping(create_tables=True)

@db_session
def get_lons():
	#note lon/lat is swapped in table..
	return db.select("select lat from data")#[:1000]

@db_session
def get_lats():
	return db.select("select lon from data")#[:1000]

@db_session
def get_mb():
	return db.select("select mb from data")#[:1000]


lons = get_lons()
lats = get_lats()
mb = get_mb()

print len(mb)


map = Basemap(projection='merc',lat_0=54.687157,lon_0=25.279652,resolution='h',  llcrnrlon=21, llcrnrlat=53.8,
    urcrnrlon=27, urcrnrlat=56.8)
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.fillcontinents(color='w',lake_color='RoyalBlue')
map.drawrivers()


x,y = map(lons, lats)
print len(x)
map.plot(x, y, markersize=1, c='k', marker='o', linestyle='None')
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary()
plt.savefig("img/map_sessions")
