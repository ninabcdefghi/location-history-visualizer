import argparse
import json
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import Image


def valid_date(s):
    '''raises error if optionally entered dates are not in a format the script can interpret'''
    try:
        stamp = int(time.mktime(datetime.strptime(
            s, "%Y-%m-%d").timetuple()) * 1000)
        if len(str(stamp)) != 13:
            msg = "ERROR: Cannot convert {} to unix timestamp.".format(s)
            raise argparse.ArgumentTypeError(msg)
        return stamp

    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def create_map(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, relief_bool, highres, width, map_dpi=300):
    '''creates the map'''
    print("Building the map. This might take a minute...")

    plt.figure(figsize=(width/map_dpi, (width * 0.69)/map_dpi), dpi=map_dpi)
    m = Basemap(projection='mill', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, resolution='l')

    if highres:
        tmpdir = '/Temp'

        size = [12000, 6000]
        Image.MAX_IMAGE_PIXELS = 233280001
        im = Image.open("HYP_HR_SR_W.tif")

        im2 = im.resize(size, Image.ANTIALIAS)
        im2.save(tmpdir+'/resized.png', "PNG")

        m.warpimage(tmpdir+'/resized.png')

    if relief_bool:
        m.shadedrelief()

    country_col = choose_border_color(relief_bool)
    m.drawcountries(color=country_col)

    m.fillcontinents(color=(0.9, 0.9, 0.9), lake_color='#FFFFFF', zorder=0)
    m.drawmapboundary(fill_color='#FFFFFF')

    return m


def choose_border_color(relief_bool):
    return (0, 0, 0, 0.5)
    # if relief_bool:
    # return (0, 0, 0, 0.5)
    # return (0.3, 0.3, 0.3, 0.5)


def plot_points(m, info, relief_bool, colorcode_list=None, title="Location History"):
    lons = []
    lats = []

    print("Almost done: Plotting the points...")

    for point in info:
        if not "altitude" in point:
            continue
        x, y = m(point['longitudeE7'] / 10**7, point['latitudeE7'] / 10**7)
        lons.append(x)
        lats.append(y)

    plot_col = choose_plot_color(relief_bool)
    plt.plot(lons, lats, color=plot_col, marker='o', markersize=2, zorder=1)

    volvlons = [38.239611, 37.473459999999996, 36.268176000000004, 34.796504999999996, 34.392028, 35.068028000000005, 35.316295000000004, 35.164190999999995, 34.349996999999995, 33.478862, 32.046261, 31.320434000000002, 30.590217, 29.627208000000003, 27.169622999999998, 25.347795, 27.208246999999997, 29.099325,
                30.285762, 31.894383, 32.656392, 33.972564, 35.679831, 35.805227, 36.467387, 36.562117, 35.757585, 35.804732, 36.682802, 35.801146, 37.104826, 37.943391999999996, 42.317561, 42.434867, 39.772249, 39.646865999999996, 37.239032, 38.568534, 37.920627, 37.49407, 38.173226, 39.727585999999995, 40.514109999999995]
    volvlats = [48.276534, 49.497679999999995, 50.008091, 48.506278, 47.440595, 46.604948, 47.001849, 47.801063, 47.076653, 48.372486, 48.836162, 48.697967999999996, 50.242515999999995, 52.559738, 56.251605000000005, 60.597143, 60.690663, 58.346371, 57.07038000000001, 54.346737, 51.645127, 51.40794,
                51.412964, 51.466957, 52.347021000000005, 53.059746999999994, 52.769012, 51.4768, 51.432404, 51.472224, 58.488110999999996, 58.348442000000006, 59.141006999999995, 59.601043999999995, 64.420735, 66.967212, 67.277521, 68.775407, 69.7915, 71.556892, 73.96901700000001, 73.24885400000001, 72.808165]

    novolvlons = [39.727585999999995, 39.694327, 39.70358, 39.499047999999995, 41.176429999999996, 43.78215, 36.61459, 30.654854999999998,
                  29.594222, 25.78974, 22.576141, 22.629853, 10.603349, 11.573236, 13.100594000000001, 12.92855, 12.572573, 13.75585, 13.757851]
    novolvlats = [73.24885400000001, 73.922437, 75.279597, 75.921746, 80.311706, 87.610449, 101.735883, 104.054938, 106.512196,
                  113.037995, 114.16185, 113.828529, 103.535278, 104.91841299999999, 103.180746, 102.495168, 101.898062, 100.530392, 100.500702]

    fvlats, fvlons = m(volvlats, volvlons)
    plt.plot(fvlats, fvlons, color=(0.93, 0.16, 0.22, 0.5),
             marker='o', markersize=2, zorder=1, linewidth=2.0)

    restlats, restlons = m(novolvlats, novolvlons)
    plt.plot(restlats, restlons, color=(0, 0, 0, 0.5),
             marker='o', markersize=2, zorder=1, linewidth=2.0)

    plt.title(title)

    return plt


def choose_plot_color(relief_bool):
    if relief_bool:
        return (0, 0, 0, 0.5)
    return (0.93, 0.16, 0.22, 0.5)


def calculate_map_boundaries(parsed_json):
    '''calculate map boundaries with some space around the most extreme points'''
    llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = find_border_points(
        parsed_json)

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


def find_border_points(parsed_json):
    '''returns most extreme latitudes and longitudes. needed for calculation of map'''
    lats = set([d['latitudeE7'] for d in parsed_json])
    lons = set([d['longitudeE7'] for d in parsed_json])

    minlat = min(lats) / 10**7
    maxlat = max(lats) / 10**7
    minlon = min(lons) / 10**7
    maxlon = max(lons) / 10**7

    print(minlat, maxlat, minlon, maxlon)
    return minlat, maxlat, minlon, maxlon


def select_from_dates(parsed_json, oldest_timestamp, newest_timestamp, start=False, end=False):
    '''selects relevant datapoints in case start and/or end date are provided'''

    if not start:
        start = oldest_timestamp
    if not end:
        end = newest_timestamp
        print(end)

    parsed_dated_json = [
        e for e in parsed_json if int(e["timestamp"]) >= start]
    parsed_dated_json = [
        e for e in parsed_dated_json if int(e["timestamp"]) <= end]

    return parsed_dated_json


def check_json_file(parsed_json):
    '''provides information about the json file used'''
    print("Done! you provided a file with {} data points.".format(len(parsed_json)))
    # timestampMS is Removed around January 2022.Replaced by timestamp Bug Fixed
    # Refernce Article "https://locationhistoryformat.com/reference/records/#:~:text=Removed%20around%20January%202022.Replaced%20by%20timestamp"
    timestamps = []

    for d in parsed_json:
        if isinstance(d['timestamp'], int):
            timestamps.append(d['timestamp'])
        else:
            timestamp = int(datetime.fromisoformat(
                d['timestamp']).timestamp() * 1000)
            timestamps.append(timestamp)

    oldest = min(timestamps)
    newest = max(timestamps)

    oldest_utc = datetime.utcfromtimestamp(
        oldest / 1000).strftime("%a, %d %b %Y")
    newest_utc = datetime.utcfromtimestamp(
        newest / 1000).strftime("%a, %d %b %Y")

    print("oldest timestamp: {}, newest: {}.".format(oldest_utc, newest_utc))
    return oldest, newest


def format_location_history(json_file):
    '''takes location history as downloaded from google and formats it
    so its data points can be evaluated'''
    print("Reading and formatting your location history...")

    try:
        with open(str(json_file)) as f:
            parsed_json = f.read()
            parsed_json = json.loads(parsed_json)
    except:
        print("ERROR 1: Sorry, not a valid google location history file! "
              "Please download it from google and try again.")
        sys.exit(1)

    try:
        parsed_json = parsed_json["locations"]
    except:
        print("ERROR 2: Sorry, not a valid google location history file! "
              "Please download it from google and try again.")
        sys.exit(1)

    return parsed_json
