#!/bin/bash

#./pullYelp.py

./makeMap.R

sed -e '/<\/head>/{r headhtml.txt' -e 'd;}' newmap.html | sed '/<div id="htmlwidget.*px;">/r bodyhtml.txt' > YelpMap.html