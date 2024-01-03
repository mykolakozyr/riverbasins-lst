# Land Surface Temperature - River Basins
The app enables discovering land surface temperature data over river basins in Europe, the USA and Australia and New Zealand. Temporal extent: 2017-01-01 till today. Library for visualizations - [Vega-Altair](https://altair-viz.github.io/index.html).


![Land Surface Temperature Demo](https://user-images.githubusercontent.com/17071295/189638606-1b3c3177-ba83-4cec-ab8a-3a2b04305af7.gif)

App is built on top of Google Earth Engine. For every selected river basin, the app calculates the mean land surface temperature value in a given area.


## Data
* Hydrological basins in Europe - [FAO Map Catalog.](https://data.apps.fao.org/map/catalog/srv/api/records/1849e279-67bd-4e6f-a789-9918925a11a1)
* Watershed Boundary Dataset in the USA - [USGS.](https://www.usgs.gov/national-hydrography/watershed-boundary-dataset)
* Hydrological basins in Australia and New Zealand - [FAO Map Catalog.](https://data.apps.fao.org/catalog/dataset/a1a0e9ee-5062-4950-a6b9-fdd2284b2607)
* Land Surface Temperature - [MODIS via Google Earth Engine.](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2)
