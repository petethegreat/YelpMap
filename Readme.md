# YelpMap

This will generate a leaflet map of Toronto displaying yelp info on local restaurants. Restaurants are colour-coded by cuisine style, with marker opacity depending on the restaurant rating (highly rated restaurants are opaque). 

## Source

  * [pullYelp.py](https://github.com/petethegreat/YelpMap/blob/master/pullYelp.py) - using the [Yelp fusion api](https://www.yelp.ca/developers/documentation/v3), pulls restaurant data from yelp and stores it in  yelpData.csv. This script expects to find either a yelp token in tokenCache.txt or api credentials in yelpCredentials.txt.
  * [makeMap.R](https://github.com/petethegreat/YelpMap/blob/master/makeMap.R) - R script (executable) that reads the .csv file and uses the R leaflet package to create the map. The html for the map is written to newmap.html
  * [mapgen.sh](https://github.com/petethegreat/YelpMap/blob/master/mapgen.sh) - bash script that runs makeMap.R, and then uses sed to add a couple other bits of html. Code from headhtml.txt is pasted into the <head> section, stuff from bodyhtml.txt is pasted into the body. The output is written to YelpMap.html, which is the "final" map. The stuff added to head is just for google analytics, the body stuff is the static yelp logo in the bottom left.
