import argparse
import json
from datetime import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import sys


def format_location_history(json_file):
	'''takes any google location history and formats it so its data points can be evaluated'''
	print("Reading and formatting your location history...")
	try:
		with open(str(json_file)) as f:
			parsed_json = f.read()
			parsed_json = json.loads(parsed_json)
	except:
		print("ERROR: Sorry, not a valid google location history file! "
			"Please download it from google and try again.")
		sys.exit(1)
    
	try:
		parsed_json = parsed_json["locations"]
	except:
		print("ERROR: Sorry, not a valid google location history file! "
			  "Please download it from google and try again.")
		sys.exit(1)

	return parsed_json


def check_json_file(parsed_json):
    '''provides information about the json file used'''
    print("Done! you provided a file with {} data points.".format(len(parsed_json)))

    timestamps = [int(d['timestampMs']) for d in parsed_json]
    oldest = datetime.utcfromtimestamp(min(timestamps) / 1000).strftime("%a, %d %b %Y")
    newest = datetime.utcfromtimestamp(max(timestamps) / 1000).strftime("%a, %d %b %Y")

    print("oldest timestamp: {}, newest: {}.".format(oldest, newest))
    return oldest, newest


def select_from_dates(parsed_json, oldest_timestamp, newest_timestamp, start=False, end=False):
	'''selects relevant datapoints in case start and/or end date are provided'''
	if not end:
		end = oldest_timestamp
	if not start:
		start = newest_timestamp

	parsed_dated_json = [e for e in parsed_json if int(e["timestampMs"]) >= start]
	parsed_dated_json = [e for e in parsed_dated_json if int(e["timestampMs"]) <= end]

	return parsed_dated_json


def find_border_points(parsed_json):
	'''returns most extreme latitudes and longitudes. needed for calculation of map'''
	lats = set([d['latitudeE7'] for d in parsed_json])
	lons = set([d['longitudeE7'] for d in parsed_json])

	return min(lats) / 10**7, (max(lats)) / 10**7, (min(lons)) / 10**7, (max(lons)) / 10**7 #besser machen


def calculate_map_boundaries(parsed_json):
	'''calculate map boundaries with some space around the most extreme points'''
	llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = find_border_points(parsed_json)
	
	add_to_lat = abs(llcrnrlat - urcrnrlat) / 20
	add_to_lon = abs(llcrnrlon - urcrnrlon) / 20

	# corrects lower end's scaling difference
	lower_lat_scale_correct = 1.9

	llcrnrlat -= (add_to_lat * lower_lat_scale_correct)
	urcrnrlat += add_to_lat
	llcrnrlon -= add_to_lon
	urcrnrlon += add_to_lon

	return llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon


def plot_points(m, info, colorcode_list=None, title="Your Location History"):
	lons = []
	lats = []

	print("Almost done: Plotting the points...")
    
	for point in info:
		if not "altitude" in point:
			continue
		x, y = m(point['longitudeE7'] / 10**7, point['latitudeE7'] / 10**7)
		lons.append(x)
		lats.append(y)

	black = (0, 0, 0, 0.5)
	plt.plot(lons, lats, color=black, marker='o', markersize=2, zorder=1)
	plt.title(title)
    
	return plt


def create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, map_dpi=200):
    '''creates the map'''
    print("Building the map. This might take a minute...")
    
    plt.figure(figsize=(5980/map_dpi, 4140/map_dpi), dpi=map_dpi)
    m = Basemap(projection='mill', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, \
            llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, resolution='f')

    m.shadedrelief()
    m.drawcountries()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF', zorder=0)
    m.drawmapboundary(fill_color='#FFFFFF')
    
    return m



def valid_date(s):
	try:
		return int(time.mktime(datetime.strptime(s, "%Y-%m-%d").timetuple()) * 1000)
		#datetime.strptime(s, "%Y-%m-%d")
	except ValueError:
		msg = "Not a valid date: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def main():
	parser = argparse.ArgumentParser(description="Enter your json file.")
	parser.add_argument("-i", "--infile", nargs=1, type=str)
	parser.add_argument("-s", "--startdate", help="Start Date - format YYYY-MM-DD", nargs=1, type=valid_date, default=False)
	parser.add_argument("-e", "--enddate", help="End Date - format YYYY-MM-DD", nargs=1, type=valid_date, default=False)
	arguments = parser.parse_args()

	#print(arguments.startdate[0])
	#print(arguments.enddate[0])


	loc_hist = format_location_history(arguments.infile[0])
	oldest_timestamp, newest_timestamp = check_json_file(loc_hist)

	if arguments.startdate or arguments.enddate:
		startdate = arguments.startdate[0]
		enddate = arguments.enddate[0]
		loc_hist = select_from_dates(loc_hist, oldest_timestamp, newest_timestamp, start=startdate, end=enddate)

	llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = calculate_map_boundaries(loc_hist)
	m = create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon)
	plot_points(m, loc_hist)

	name = 'your_map{}.png'.format(str(int(time.time())))
	plt.savefig(name)
	print("Done. Saved the map as {}; bye.".format(name))


if __name__ == "__main__":
	main()