# Location History Visualizer

```
██╗      ██████╗  ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗      ███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗ 
██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║      ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║     ██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║█████╗██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
██║     ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════╝██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║      ██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝


[*] Google Location Mapper 
[*] Vist `https://takeout.google.com/` get you location
[*] Version 1.1.2
[*] Github Repo 'https://github.com/mrintroverrt/Location-History-Visualizer'
```

## Description

**Location History Visualizer** is a command-line tool that creates simple maps from Google Location History data. It allows users to generate visualizations of their historical location data, providing insights into travel patterns and visitation frequency.

## Features

- Generate maps from Google Location History data.
- Filter data by start and end dates.
- Customize map title and width.
- Landscape feature and high-resolution map options.

## Usage

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/location-history-visualizer.git
   cd location-history-visualizer

## Installation

`$ pip install -r requirements.txt`
## Basic Usage

Run the script with the following command-line arguments
`python Lctaion-Mapper.py -i Records.json -s 2022-01-01 -e 2022-12-31 -t "My Location History" -w 1200 -relief -highres`
## Arguments
* `-i` or `--infile:` Path to the JSON file downloaded from Google Takeout.
* `-s` or `--startdate:` Start date in YYYY-MM-DD format for data filtering.
* `-e` or `--enddate:` End date in YYYY-MM-DD format for data filtering.
* `-t` or `--title:` Custom title for the Generated map
* `-w` or `--width:` Map width in pixels (default: 6000)
* `-relief:` Show landscape features on the map
* `-highres:` Generate a high-resolution shaded relief map.
## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License. See the LICENSE file for details.
## Acknowledgments
* Inspired by the need to visualize personal location history data.
* We appreciate the contributions and feedback from the open-source community