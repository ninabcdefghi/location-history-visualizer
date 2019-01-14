import argparse
import json
from datetime import datetime
import math
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import sys


def format_location_history(json_file):
	'''takes any google location history and formats it so its data points can be evaluated'''
	print("Reading and formatting your location history: This might take a minute...")
	try:
		with open(str(json_file)) as f:
			parsed_json = f.read()
			parsed_json = json.loads(parsed_json)
	except:
		print("Sorry, not a valid google location history file! "
			"Please download it from google and try again.")
		sys.exit(1)
    
	try:
		parsed_json = parsed_json["locations"] 
	except:
		print("Sorry, not a valid google location history file! "
			  "Please download it from google and try again.")
		sys.exit(1)

	return parsed_json


def check_json_file(parsed_json):
    '''provides information about the json file used'''
    print("Done! you provided a file with {} data points.".format(len(parsed_json)))
    timestamps = [int(d['timestampMs']) for d in parsed_json]
    oldest = datetime.fromtimestamp(min(timestamps) / 1000)
    newest = datetime.fromtimestamp(max(timestamps) / 1000)
    print("oldest timestamp: {}, newest: {}.".format(oldest, newest))


def deg_to_radian(deg):
    '''converts late7 and lone7 from degree to radian'''
    deg = deg / 10 ** 7
    return deg * (math.pi / 180.0)


def find_border_points(parsed_json):
	'''returns most extreme latitudes and longitudes. needed for calculation of map'''
	lats = set([d['latitudeE7'] for d in parsed_json])
	lons = set([d['longitudeE7'] for d in parsed_json])
	return min(lats) / 10**7, (max(lats)) / 10**7, (min(lons)) / 10**7, (max(lons)) / 10**7


def calculate_map_boundaries(m):
	'''calculate map boundaries from that'''
	return 0


def plot_points(m, info, colorcode_list=None):
    lons = []
    lats = []
    
    for point in info:
        if not "altitude" in point:
            continue
        x, y = m(point['longitudeE7'] / 10**7, point['latitudeE7'] / 10**7)
        lons.append(x)
        lats.append(y)

    if not colorcode_list == None: 
    	plt.scatter(lons, lats, c=colorcode_list, alpha=1.0, zorder=2)

    plt.plot(lons, lats, color='#fee5d9', marker='o', markersize=3, zorder=1)

    # plt.title("choose a title")
    
    return plt.show()


def create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, map_dpi=96):
    '''creates the map'''
    print("Building the map. This might take an even longer minute...")
    
    plt.figure(figsize=(2600/map_dpi, 1800/map_dpi), dpi=map_dpi)
    m = Basemap(projection='mill',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,\
            llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,resolution='i')
    
    m.shadedrelief()
    m.drawcountries()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF', zorder=0)
    m.drawmapboundary(fill_color='#FFFFFF')
    
    return m


def main():
	parser = argparse.ArgumentParser(description="Enter your json file.")
	parser.add_argument('--infile', nargs=1, type=str)
	parser.add_argument("-alt", "--altitude_marker", default=False)
	arguments = parser.parse_args()
	loc_hist = format_location_history(arguments.infile[0])
	check_json_file(loc_hist) # parsed json!
	llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = find_border_points(loc_hist)
	m = create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon)

	name = 'your_map{}.png'.format(str(int(time.time())))
	plt.savefig(name)
	print("Done. Saved the map as {}; bye.".format(name))

if __name__ == "__main__":
	main()