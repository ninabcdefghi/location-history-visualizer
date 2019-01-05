import argparse
import json


def prepare_location_history(json_file):
	'''takes any google location history and formats it so its data points can be evaluated'''
	with open(str(json_file)) as f:
		info = f.read()
		info = json.loads(info)
    
	try:
		info = info["locations"] 
	except:
		pass

	return info

parser = argparse.ArgumentParser(description="Enter your json file.")
parser.add_argument('--infile', nargs=1,
                    type=str) #type=str?
arguments = parser.parse_args()

loc_hist = prepare_location_history(arguments.infile[0])
print(loc_hist) # parsed json