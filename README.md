# Land Surface Temperature - River Basins
The app enables discovering land surface temperature data over river basins in Europe. Temporal extent: 2017-01-01 till today. Library for visualizations - [Vega-Altair](https://altair-viz.github.io/index.html).


![Land Surface Temperature Demo](https://user-images.githubusercontent.com/17071295/189638606-1b3c3177-ba83-4cec-ab8a-3a2b04305af7.gif)

App is built on top of Google Earth Engine. For every selected river basin, the app calculates the mean land surface temperature value in a given area.


## Data
- Hydrological basins in Europe - [FAO Map Catalog](https://data.review.fao.org/map/catalog/srv/api/records/1849e279-67bd-4e6f-a789-9918925a11a1).
- Land Surface Temperature - [MODIS via Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2).
