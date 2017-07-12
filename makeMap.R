#!/usr/bin/Rscript

# MakeMap.R
library(leaflet)
library(RColorBrewer)
library(htmltools)
library(htmlwidgets)
data<-read.csv('yelpData.csv')
#data[1:2,]
# dim(data)

# set up marker colours
pal<-colorFactor('Set1',domain=levels(data$category))
# define a function to get the stars image based on rating

# get stars image based on rating
# looks like ratings are in multiples of 0.5, could probably simplify this
data$starsimage=""
data$starsimage[data$rating < 1.0] <- '<img src="assets/small_0.png">'
data$starsimage[data$rating >= 1.0 & data$rating < 1.5] <- '<img src="assets/small_1.png">'
data$starsimage[data$rating >= 1.5 & data$rating < 2.0] <- '<img src="assets/small_1_half.png">'
data$starsimage[data$rating >= 2.0 & data$rating < 2.5] <- '<img src="assets/small_2.png">'
data$starsimage[data$rating >= 2.5 & data$rating < 3.0] <- '<img src="assets/small_2_half.png">'
data$starsimage[data$rating >= 3.0 & data$rating < 3.5] <- '<img src="assets/small_3.png">'
data$starsimage[data$rating >= 3.5 & data$rating < 4.0] <- '<img src="assets/small_3_half.png">'
data$starsimage[data$rating >= 4.0 & data$rating < 4.5] <- '<img src="assets/small_4.png">'
data$starsimage[data$rating >= 4.5 & data$rating < 4.95] <- '<img src="assets/small_4_half.png">'
data$starsimage[data$rating >= 4.95] <- '<img src="assets/small_5.png">'

#popup content
data$content<-paste(sep='<br/>',paste(sep='','<a href="https://www.yelp.ca/biz/',data$yelpid,'">',data$name,'</a>'),data$starsimage,data$rating,paste(data$reviews,'reviews'))

data$category <- as.factor(data$category)

streetprovider<-providers$CartoDB.PositronNoLabels
labelprovider<-providers$CartoDB.PositronOnlyLabels
# providers$Stamen.TonerLabels
map<- leaflet(data=data) %>% setView(lng = -79.4, lat = 43.65, zoom = 12) %>%
  #addTiles() %>% 
  addProviderTiles(streetprovider,
                   options = providerTileOptions(opacity = 0.45)) %>%
  addProviderTiles(labelprovider) %>%
  addCircleMarkers(color=~pal(category),
                   stroke=FALSE,
                   fillOpacity=~rating/5.0,
                   # clusterOptions=markerClusterOptions(),
                   label=~name, #htmlEscape(name)
                   group=~category,
                   popup=~content,
                   popupOptions=popupOptions(minWidth=100)	
  ) %>%
  addLayersControl(
    overlayGroups = levels(data$category),
    options = layersControlOptions(collapsed = FALSE)
  ) %>%
  addLegend("topright",pal=pal,values=levels(data$category))

saveWidget(map, file="newmap.html")
