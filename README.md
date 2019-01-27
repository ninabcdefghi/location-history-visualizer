# Location History Visualizer
Simple Python CLI tool enabling anyone to visualize the location history that google maps collects - data most likely being collected [whether you want it or not](https://www.independent.co.uk/news/world/americas/google-location-data-privacy-android-sundar-pichai-a8490636.html).

<img src="/outputexamples/basic_example.jpg" alt="output preview_basic" width="350" height="252"> <img src="/outputexamples/relief_example.jpg" alt="output preview_relief" width="350" height="252">

# Installation
```
pip install -r requirements.txt
```

# Basic Usage
- First, [download your own location history here](https://takeout.google.com/) (deselect all, then select "Location History"). Download the archive and unzip the .json file.
- Open your command line, go to the Location History Visualizer's path and type `python location-history-visualizer.py -i name_and_path_of_your.json`. This gives you a simple visualization of your data.

# Optional Arguments
- Relief: If the `-relief` is set, the output map will show landscape features. Takes a bit longer to generate.
- Start date: `-s YYYY-MM-DD` lets you specify a date from which the visualization should be produced.
- End date: `-e YYYY-MM-DD` sets an end date.
- Width: `-w 6000` adjusts the width of the output image flexibly. Choose a higher integer for more detailed output, a lower for faster output.
- Title: `-t CHOOSE TITLE` gives your map a custom title.

# Output
The map can be used to [create detailed relief](/outputexamples/relief_big.jpg) or [schematic maps of your entire data](/outputexamples/basic_big.jpg) and to [visualize itineraries](/outputexamples/reliefdetail3.jpg).

![relief_big](/outputexamples/reliefdetail2.jpg)
