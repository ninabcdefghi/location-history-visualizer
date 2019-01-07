import argparse
import json
from datetime import datetime
import math
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def format_location_history(json_file):
	'''takes any google location history and formats it so its data points can be evaluated'''
	print("Reading and formatting your location history: This might take a minute...")
	with open(str(json_file)) as f:
		parsed_json = f.read()
		parsed_json = json.loads(parsed_json)
    
	try:
		parsed_json = parsed_json["locations"] 
	except:
		print("Sorry, not a valid google location history file! "
			  "Please download it from google and try again.")
		exit

	return parsed_json


def check_json_file(parsed_json):
    '''provides information about the json file used'''
    print("Done! you provided a file with {} data points.".format(len(parsed_json)))
    timestamps = [int(d['timestampMs']) for d in parsed_json]
    oldest = datetime.fromtimestamp(min(timestamps) / 1000)
    newest = datetime.fromtimestamp(max(timestamps) / 1000)
    print("oldest timestamp: {}, newest: {}.".format(oldest, newest))


def find_border_points(parsed_json):
	'''returns most extreme latitudes and longitudes. needed for calculation of map'''
	lats = set([d['latitudeE7'] for d in parsed_json])
	lons = set([d['longitudeE7'] for d in parsed_json])
	return min(lats), max(lats), min(lons), max(lons)


def calculate_map_boundaries(m):
	'''calculate map boundaries from that'''
	return 0


def create_map(map_dpi=96):
    '''creates the map'''
    print("Building the map...")
    plt.figure(figsize=(2600/map_dpi, 1800/map_dpi), dpi=map_dpi)
    m = Basemap(projection='mill',llcrnrlat=25.1,urcrnrlat=71.5,\
            llcrnrlon=-10.5,urcrnrlon=87.3,resolution='i')
    
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
	minlat, maxlat, minlon, maxlon = find_border_points(loc_hist)
	print("minlat: ", minlat, "maxlat: ", maxlat, "minlon: ", minlon, "maxlon: ", maxlon)


if __name__ == "__main__":
	main()