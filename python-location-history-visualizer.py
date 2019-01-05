import argparse
import json

parser = argparse.ArgumentParser(description="Enter your json file.")
parser.add_argument('--infile', nargs=1,
                    help="JSON file to be processed",
                    type=argparse.FileType('r'))

arguments = parser.parse_args()

# TO DO: parse it as json...
d = vars(arguments)

print(d)