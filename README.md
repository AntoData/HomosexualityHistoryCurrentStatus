# HomosexualityHistoryCurrentStatus
 In this project we use folium, pandas and webscraping using requests and beautifulSoup to create a map that contains information about the legal status of homosexuality around the world. We created an API with a function called buildMap to create the map with the colors combining number ranges and static string values to color that map. Also we use request and beautifulSoup to get and parse all the wikipedia pages that contain information about lgbt rights in each country for the html we display when we open a marker (every country has a marker placed in its capital to display with information).

In this project we generate an html files:
- homosexuality_world_history_and_status_worldwide.html: It's a map that represents with different shades of green in which year homosexuality was decriminalized in each country (range of numbers), red for countries where homosexuality is punished with prison, dark red for countries where homosexuality is punished with a life-long prison sentence and purple for countries where the punishment is death penalty and blue for countries where homosexuality has never seen ilegal (static string values). Also, the map includes a marker placed in the capital city of each country. If you open it, information taken from wikipedia about lgtb rights in that country

The project is organized in several folders
 
Folder API, contains two interesting modules:
- MapGenerator whose function build_map allows you to build a map coloring regions according to certain values defined by yourself and including a legend and putGenericMarkers that allows you to set markers in the map and the HTML code you want to be displayed when we open a marker

Folder Wrapper, contains Wrappers for the previously mentioned modules:
- DecriminalizationHomosexualityWrapper: Contains functions that will be used in the module DecriminalizationStatusHomosexualityWorldwide.py that will call the functions buildMap and putGenericMarkers customizing them.

Folder Instantiators, contains the modules we have to run to generate the maps that use the modules in API and also the modules in API:
- DecriminalizationStatusHomosexualityWorldwide.py: When you run it, it will generate the file homosexuality_world_history_and_status_worldwide.html

Folder Data:
Here we will include all the csvs, xlxs and so on files that we need to get the information for our maps and graphs
