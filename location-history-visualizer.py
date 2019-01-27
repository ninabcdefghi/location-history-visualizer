import argparse
import json
from datetime import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import sys


def format_location_history(json_file):
	'''takes location history as downloaded from google and formats it
	so its data points can be evaluated'''
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

    oldest = min(timestamps)
    newest = max(timestamps)

    oldest_utc = datetime.utcfromtimestamp(oldest / 1000).strftime("%a, %d %b %Y")
    newest_utc = datetime.utcfromtimestamp(newest / 1000).strftime("%a, %d %b %Y")

    print("oldest timestamp: {}, newest: {}.".format(oldest_utc, newest_utc))
    return oldest, newest


def select_from_dates(parsed_json, oldest_timestamp, newest_timestamp, start=False, end=False):
	'''selects relevant datapoints in case start and/or end date are provided'''
	
	if not start:
		start = oldest_timestamp
	if not end:
		end = newest_timestamp
		print(end)

	parsed_dated_json = [e for e in parsed_json if int(e["timestampMs"]) >= start]
	parsed_dated_json = [e for e in parsed_dated_json if int(e["timestampMs"]) <= end]

	return parsed_dated_json


def find_border_points(parsed_json):
	'''returns most extreme latitudes and longitudes. needed for calculation of map'''
	lats = set([d['latitudeE7'] for d in parsed_json])
	lons = set([d['longitudeE7'] for d in parsed_json])

	minlat = min(lats) / 10**7
	maxlat = max(lats) / 10**7
	minlon = min(lons) / 10**7
	maxlon = max(lons) / 10**7

	return minlat, maxlat, minlon, maxlon


def calculate_map_boundaries(parsed_json):
	'''calculate map boundaries with some space around the most extreme points'''
	llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = find_border_points(parsed_json)
	
	# determines how many percent of map is shown in addition to extreme points 
	padding = 0.05

	add_to_lat = abs(llcrnrlat - urcrnrlat) * padding
	add_to_lon = abs(llcrnrlon - urcrnrlon) * padding

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


def create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, width, map_dpi=300):
    '''creates the map'''
    print("Building the map. This might take a minute...")
    
    plt.figure(figsize=(width/map_dpi, (width * 0.69)/map_dpi), dpi=map_dpi)
    m = Basemap(projection='mill', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, \
            llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, width=width, resolution='l')

    m.shadedrelief()
    m.drawcountries()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF', zorder=0)
    m.drawmapboundary(fill_color='#FFFFFF')
    
    return m


def valid_date(s):
	'''raises error if optionally entered dates are not in a format the script can interpret'''
	try:
		stamp = int(time.mktime(datetime.strptime(s, "%Y-%m-%d").timetuple()) * 1000)
		if len(str(stamp)) != 13:
			msg = "ERROR: Cannot convert {} to unix timestamp.".format(s)
			raise argparse.ArgumentTypeError(msg)
		return stamp

	except ValueError:
		msg = "Not a valid date: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)


def main():
	parser = argparse.ArgumentParser(description=("Location History Visualizer: "
									"Creates simple maps from google location history."))
	parser.add_argument("-i", "--infile", nargs=1, type=str, required=True, 
						help=("Enter the name or path of the json file downloaded "
							"from google takeout, e.g. 'Location_History.json'."))
	parser.add_argument("-s", "--startdate", help="Start Date - format YYYY-MM-DD", nargs=1, 
						type=valid_date, default=False)
	parser.add_argument("-e", "--enddate", help="End Date - format YYYY-MM-DD", nargs=1, 
						type=valid_date, default=False)
	parser.add_argument("-t", "--title", help="Enter a title for your map.", type=str, 
						default=False)
	parser.add_argument("-w", "--width", help="Width of your map in pixels. Enter an integer",
						type=int, default=6000) # make it work!
	arguments = parser.parse_args()

	loc_hist = format_location_history(arguments.infile[0])
	oldest_timestamp, newest_timestamp = check_json_file(loc_hist)


	if arguments.startdate:
		startdate = arguments.startdate[0]
	else:
		startdate = int(oldest_timestamp)

	if arguments.enddate:
		enddate = arguments.enddate[0]
	else:
		enddate = int(newest_timestamp)

	if startdate != oldest_timestamp or enddate != newest_timestamp:
		loc_hist = select_from_dates(loc_hist, oldest_timestamp, newest_timestamp, 
									 start=startdate, end=enddate)


	llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = calculate_map_boundaries(loc_hist)
	
	m = create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, width=arguments.width)
	plot_points(m, loc_hist)	

	name = 'your_map{}.png'.format(str(int(time.time())))
	plt.savefig(name)
	print("Done. Saved the map as {}; bye.".format(name))


if __name__ == "__main__":
	main()