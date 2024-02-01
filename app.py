import streamlit as st
import json
import geojson
import ee
import pandas as pd
import geopandas as gpd
import altair as alt
from streamlit_folium import folium_static 
import folium
from shapely.geometry import shape



MAP_EMOJI_URL = "https://em-content.zobj.net/source/apple/354/thermometer_1f321-fe0f.png"

# Set page title and favicon.
st.set_page_config(
    page_title="Land Surface Temperature - River Basins", 
    page_icon=MAP_EMOJI_URL,
    layout="wide"
)

# Initialize session state
# if 'dropdown_values' not in st.session_state:
#     st.session_state.dropdown_values = {'region_name': None, 'maj_name': None, 'sub_name': None}


col1, col2, col3 = st.columns([1, 4, 1])
# Display header.
col2.markdown("<br>", unsafe_allow_html=True)
col2.image(MAP_EMOJI_URL, width=80)
col2.markdown("""
    # Land Surface Temperature - River Basins
    [![Follow](https://img.shields.io/twitter/follow/mykolakozyr?style=social)](https://www.twitter.com/mykolakozyr)
    [![Follow](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/mykolakozyr/)
    
    ## Details

    The app enables discovering land surface temperature data over river (hydrological) basins. 

    Temporal extent: 2017-01-01 till today.
    Library for visualizations - [Vega-Altair](https://altair-viz.github.io/index.html).

    ---
    """)

json_data = '''
{
  "type": "service_account",
  "project_id": "ee-mykolakozyr",
  "private_key_id": "379377b141b4dbfad12cf25f7ae258da74515744",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3WFncFeqIGB65\n3VsC04L9QNtMo9jaRBO+ORU40G1h1jM/RGBeaiXiXmr4t2WWr/AC0gjT4A0b+zpD\n0ZCjwLsMRPwv6IC/dbri/RjHX2DkkTwNB+0pLIRwGYQDJeJL74FiVimfFrAj2TM0\n/QYitG2aHpGf9+jvmev6yBKPE3Sj7yoC8LKikpw/jsQCvFg4KAMQMcmvsteWcpO6\nljrmuVCxiCZuJKqq0BcsZ1X6+cQSVki2ijOsfs9yshDsVO8l6MNENWqy27RvsK/S\npBXB1TrB/kK+UUucXK2s7zIVTy4rSHAyC1P+Hz/I6O0mXORvVrkekANKhRsOdKvK\nzlVw80eJAgMBAAECggEASjj/L8TDjFLPZYkCBhPgTGwMG2udJ0c2AuUS/UwLa/cO\nCgfBR5eLPKfigEumWalh7ZJftn5WcER1Iu1cs54bWu02dqKWNGwRu0Cg3l1zWTSe\nbdwOm4OFHeiGc8vLX9hWtZuR//BsYCbWvxXLfRMz55eGdo8jApR6XqzOLpO+vXou\nS0xTF4ci/VypA29fB2RGW4ZM4AbfY09kV4x9QjLoefPdhQxzLPSMM4jhNY9rSKbC\n6ep0xkRtDCHysaQ6rJfUwuNMXBFdSSO01pn6d0sUi4YQDqgBvFi+smr0t2AjEPNL\nSlku+OXNPBggKYhkHhKfWVrpLzAL6O+Zr0f057tPvQKBgQDZDsZgcgRnPU3EG3W5\ndyk9r5s4Hfq47wcj5eviize7ju0yIMJct0wLxtzmtcJL+f7JRbi6iEN44wiz9lIG\nnD6W+gxmkOw32i8Xjz5mQ8t6XkS9M3oOwZ2YSn9Vp4+q9dFkyxaoraKbZNkVqj5O\n3mIzX/iNWqg1w7ZzRG49OvEjvwKBgQDYPTF8j2xS+Vxe1wNwTjJxva0dXLC0iorF\nUn29QFeml3s+KrmKLUwWgvg+ZzRQvFtI0gAU0B5lwMt29aezvVmb/YHc0ZIlyRwR\nOKZfUzhFdsaZp1zko5tct/q/rk1KwE1jGLdife+v3VjzTnRjJ6g7kADaPQFPdgiZ\nglEKSlPGtwKBgQDAOk2FbHRp2ejdHFSOA/IKJ1MXx7UbwtRX/m+BGjopaNK36js3\nUT2P0HYh/CYukyAJsC2BRNw8WxSCDEtof0cO/jOtQftxG1FJVBq3BqNVo9bMmKIo\nH2AqVw+eE98wULM4yIMwr1WquQ1oGnVD876UMRI2XWtK8iDKxHe80k5skQKBgFpS\nBQ+QIKDvwyNiD++i2fMkVODEzJI8pAYTlK2t6G6PK00mL2WF0hg9EE+QcAuhAUgD\nX0FSRMAfrVy88xVia8F6O/nuF2ts+yo+TU/XxNNO71lSzLw7kjNCLZxOw74LYMeZ\nlU+wZqNAg1ztUjPwZpaqaZC+loOIO8NS6WKw9Rk1AoGBAIt0lXU+gsMiXsedZ1Vf\nDwWaydTAAXa6yyQbJnhBx8W7tpabo0Cd/XBABdt7AhSMn7xaHcMY+LUBfvTVBc2q\nSqYOlmpWHmhEoVtq361sA+hoo+UffzN3wWabTiHiu2c/rcTNHi0F8r8RZqcWqG/H\nxXksw87ackunegxJk7ygoewy\n-----END PRIVATE KEY-----\n",
  "client_email": "streamlit-gee@ee-mykolakozyr.iam.gserviceaccount.com",
  "client_id": "118001670119328519368",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-gee%40ee-mykolakozyr.iam.gserviceaccount.com"
}
'''

service_account = 'streamlit-gee@ee-mykolakozyr.iam.gserviceaccount.com'

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_gdf(gdf):
    gdf['geometry'] = gdf['geometry'].astype('geometry') 
    gdf['Timestamp'] = gdf['Timestamp'].astype(str)
    return gdf.to_json()

# json_data = st.secrets["json_data"]
# service_account = st.secrets["service_account"]


json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)

import src.gee as gee

# Defining the temporal extent of the discovery
today = ee.Date(pd.to_datetime('today'))
date_range = ee.DateRange('2017-01-01', today)

# Interface to select the area of interest.
region_name = col2.selectbox('Select the region.', ['Europe','USA', 'Australia and New Zealand', 'Near East', 'Southeast Asia'], key='region_name')
# Select the region
if region_name:
    #st.session_state.dropdown_values['region_name'] = region_name
    # Defining the GeoDataFrame with a subset of areas with archive coverage.
    filename = "data/basins_" + region_name.lower() + "_mult.geojson"
    file = open(filename)
    gdf = gpd.read_file(file)
    maj_name = col2.selectbox('Select the major hydrological basin.', sorted(pd.unique(gdf['MAJ_NAME'])), key='maj_name')
    # Select the major hydrological basin
    if maj_name:
        #st.session_state.dropdown_values['maj_name'] = maj_name
        # Select the sub-basin.
        sub_name = col2.selectbox('Select the river basin within the major one', sorted(gdf[gdf['MAJ_NAME'] == maj_name]['SUB_NAME']), key='sub_name')
            # with col2.expander('Additional parameters', expanded=False):
            #     st.text('How many charts do you want to create?')
            #     agree = st.checkbox('Yes', value='Yes', disabled=True)
            # if agree == True:
        #st.session_state.dropdown_values['sub_name'] = sub_name
        if col2.button('Discover the Land Surface Temperature data!'):
            with col2:
                with st.spinner("Collecting data using Google Earth Engine..."):
                    # Defining the geometry from the selected basin.
                    aoi_json = json.loads(gdf.loc[gdf['SUB_NAME'] == sub_name, 'geometry'].to_json())['features'][0]['geometry']
                    aoi = ee.FeatureCollection(ee.Geometry(aoi_json)).geometry()
                    # Getting LST data.
                    lst = ee.ImageCollection('MODIS/061/MOD11A2').filterDate(date_range).select('LST_Day_1km')
                    reduce_lst = gee.create_reduce_region_function(geometry=aoi, reducer=ee.Reducer.mean(), scale=1000, crs='EPSG:4326')
                    lst_stat_fc = ee.FeatureCollection(lst.map(reduce_lst)).filter(ee.Filter.notNull(lst.first().bandNames()))
                    lst_dict = gee.fc_to_dict(lst_stat_fc).getInfo()
                    lst_df = pd.DataFrame(lst_dict)
                    lst_df['LST_Day_1km'] = (lst_df['LST_Day_1km'] * 0.02 - 273.5)
                    lst_df = gee.add_date_info(lst_df)

                    # Feature to preview the geometry.
                    with st.expander('Geometry Preview', expanded=False):
                        map_aoi = folium.Map(tiles="OpenStreetMap")
                        folium.Choropleth(geo_data = aoi_json, reset=True).add_to(map_aoi)
                        bounds = map_aoi.get_bounds()
                        map_aoi.fit_bounds(bounds)
                        # Not working properly for unknown reason. To be discovered.
                        st.warning("Sometimes the map does not zoom to the selected area most likely because of [this issue](https://github.com/randyzwitch/streamlit-folium/issues/152).")
                        folium_static(map_aoi)

            # Creating Charts
            # Line Chart with Points: https://altair-viz.github.io/gallery/line_chart_with_points.html
            line_chart = alt.Chart(lst_df).mark_line(
                point=alt.OverlayMarkDef(color="red")
            ).encode(
                alt.X("Timestamp"),
                alt.Y("LST_Day_1km", title='Land Surface Temperature, °C'),
            ).interactive()

            # Ridgeline plot Example: https://altair-viz.github.io/gallery/ridgeline_plot.html
            step = 16
            overlap = 1

            ridgeline_plot = alt.Chart(lst_df, height=step).transform_timeunit(
                Month="month(Timestamp)"
            ).transform_joinaggregate(
                mean_temp="mean(LST_Day_1km)", groupby=['Month']
            ).transform_bin(
                ['bin_max', 'bin_min'], 'mean_temp'
            ).transform_aggregate(
                value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
            ).transform_impute(
                impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
            ).mark_area(
                interpolate='monotone',
                fillOpacity=0.8,
                stroke='lightgray',
                strokeWidth=0.5
            ).encode(
                alt.X('bin_min:Q', bin='binned',
                    title='Land Surface Temperature, °C'
                ),
                alt.Y(
                    'value:Q',
                    scale=alt.Scale(range=[step, -step * overlap]),
                    axis=None
                ),
                alt.Fill(
                    'mean_temp:Q',
                    legend=None,
                    scale=alt.Scale(domain=[40, -5], scheme='redyellowblue')
                )
            ).facet(
                row=alt.Row(
                    "Month:T",
                    title=None,
                    header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
                )
            ).properties(
                bounds='flush'
            ).configure_facet(
                spacing=0
            ).configure_view(
                stroke=None
            ).configure_title(
                anchor='end'
            )

            # Binned Heatmap: https://altair-viz.github.io/gallery/binned_heatmap.html
            binned_heatmap = alt.Chart(lst_df).mark_rect().encode(
                alt.X("Month:O"),
                alt.Y("Year:O"),
                alt.Color("mean(LST_Day_1km):Q", scale=alt.Scale(scheme='redyellowblue', reverse=True), title='Land Surface Temperature, °C')
            ).interactive()

            # Violin Plot Chart: https://altair-viz.github.io/gallery/violin_plot.html
            violin_chart = alt.Chart(lst_df).transform_density(
                "LST_Day_1km",
                as_=["LST_Day_1km", 'density'],
                extent=[-20, 60],
                groupby=["Year"]
            ).mark_area(orient='horizontal').encode(
                alt.Y("LST_Day_1km:Q",title='Land Surface Temperature, °C'),
                color="Year:N",
                x=alt.X(
                    'density:Q',
                    stack='center',
                    impute=None,
                    title=None,
                    axis=alt.Axis(labels=False, values=[0],grid=False, ticks=True),
                ),
                column=alt.Column(
                    "Year:Q",
                    header=alt.Header(
                        titleOrient='bottom',
                        labelOrient='bottom',
                        labelPadding=0,
                    ),
                )
            ).properties(
                width=100,
                height=450
            ).configure_facet(
                spacing=0
            ).configure_view(
                stroke=None
            )

            # Hexbin Chart: https://altair-viz.github.io/gallery/hexbins.html
            # Size of the hexbins
            size = 15
            # Count of distinct x features
            xFeaturesCount = 12
            # Count of distinct y features
            yFeaturesCount = 6
            yField = 'Timestamp'
            xField = 'Timestamp'
            # the shape of a hexagon
            hexagon = "M0,-2.3094010768L2,-1.1547005384 2,1.1547005384 0,2.3094010768 -2,1.1547005384 -2,-1.1547005384Z"
            hexbin_chart = alt.Chart(lst_df).mark_point(size=size**2, shape=hexagon).encode(
                x=alt.X('xFeaturePos:Q', axis=alt.Axis(title='Month',
                                                       grid=False, tickOpacity=0, domainOpacity=0)),
                y=alt.Y('year(' + yField + '):O', axis=alt.Axis(title='Year',
                                                               labelPadding=20, tickOpacity=0, domainOpacity=0)),
                stroke=alt.value('black'),
                strokeWidth=alt.value(0.2),
                fill=alt.Color('mean(LST_Day_1km):Q', scale=alt.Scale(scheme='redyellowblue', reverse=True), title='Land Surface Temperature, °C'),
                tooltip=['Month:O', 'Year:O', 'mean(LST_Day_1km):Q']
            ).transform_calculate(
                # This field is required for the hexagonal X-Offset
                xFeaturePos='(year(datum.' + yField + ') % 2) / 2 + month(datum.' + xField + ')'
            ).properties(
                # Scaling factors to make the hexbins fit. Adjusted to the streamlit view
                width=size * xFeaturesCount * 3.6,
                height=size * yFeaturesCount * 2.77128129216
            ).configure_view(
                strokeWidth=0
            ).interactive()

            # Boxplot Chart: https://altair-viz.github.io/gallery/boxplot.html
            boxplot_chart_year = alt.Chart(lst_df).mark_boxplot(extent='min-max').encode(
                alt.X('Year:O'),
                alt.Y('mean(LST_Day_1km):Q',title='Land Surface Temperature, °C')
            ).interactive()

            # Boxplot Chart: https://altair-viz.github.io/gallery/boxplot.html
            boxplot_chart_month = alt.Chart(lst_df).mark_boxplot(extent='min-max').encode(
                alt.X('Month:O'),
                alt.Y('mean(LST_Day_1km):Q', title='Land Surface Temperature, °C')
            ).properties(height=500).interactive()

            # Scatter Plot Chart: https://altair-viz.github.io/gallery/scatter_tooltips.html
            scatter_chart = alt.Chart(lst_df).mark_circle(size=60).encode(
                alt.Y('LST_Day_1km', title='Land Surface Temperature, °C'),
                alt.X('DOY', title='Day of the Year'),
                color='Year:N',
                tooltip=['LST_Day_1km', 'Timestamp']
            ).interactive()

            # Bar Chart with Negative Values: https://altair-viz.github.io/gallery/bar_chart_with_negatives.html
            bar_negative = alt.Chart(lst_df).mark_bar().encode(
                alt.X("Timestamp"),
                alt.Y("LST_Day_1km:Q", title='Land Surface Temperature, °C'),
                color=alt.condition(
                    alt.datum.LST_Day_1km > 0,
                    alt.value("orange"),  # The positive color
                    alt.value("steelblue")  # The negative color
                )
            ).interactive()

            # Binned Scatterplot: https://altair-viz.github.io/gallery/binned_scatterplot.html
            scatter_binned = alt.Chart(lst_df).mark_circle().encode(
                alt.X('DOY:Q', bin=True, title='Day of the Year'),
                alt.Y('LST_Day_1km:Q', bin=True, title='Land Surface Temperature, °C'),
                size='count()'
            ).interactive()

            #Scatter Plot with LOESS Lines: https://altair-viz.github.io/gallery/scatter_with_loess.html
            base_scatter = alt.Chart(lst_df).mark_circle(opacity=0.5).encode(
                alt.X('DOY', title='Day of the Year'),
                alt.Y('LST_Day_1km:Q', title='Land Surface Temperature, °C'),
                alt.Color('Year:N')
            )
            scatter_loess = base_scatter + base_scatter.transform_loess('DOY', 'LST_Day_1km', groupby=['Year']).mark_line(size=4).interactive()

            # Stripplot: https://altair-viz.github.io/gallery/stripplot.html
            stripplot =  alt.Chart(lst_df, width=40).mark_circle(size=8).encode(
                x=alt.X(
                    'jitter:Q',
                    title=None,
                    axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
                    scale=alt.Scale(),
                ),
                y=alt.Y('LST_Day_1km:Q', title='Land Surface Temperature, °C'),
                color=alt.Color('Year:N', legend=None),
                column=alt.Column(
                    'Year:N',
                    header=alt.Header(
                        labelAngle=-90,
                        titleOrient='top',
                        labelOrient='bottom',
                        labelAlign='right',
                        labelPadding=3,
                    ),
                ),
            ).transform_calculate(
                # Generate Gaussian jitter with a Box-Muller transform
                jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
            ).configure_facet(
                spacing=0
            ).configure_view(
                stroke=None
            ).properties(height=400).interactive()

            # Table Bubble Plot: https://altair-viz.github.io/gallery/table_bubble_plot_github.html
            table_bubble = alt.Chart(lst_df).mark_circle().encode(
                alt.X('Month:O'),
                alt.Y('Year:O'),
                alt.Size('mean(LST_Day_1km):Q', title='Land Surface Temperature, °C')
            ).interactive()


            # Visualizing in the defined layout
            # Row 1
            col1, col2 = st.columns([4,1])
            with col1:
                st.altair_chart(line_chart, use_container_width=True)
            with col2:
                st.altair_chart(boxplot_chart_year, use_container_width=True)

            # Row 2
            col1, col2 = st.columns([1,1])
            with col1:
                st.altair_chart(binned_heatmap, use_container_width=True)
            with col2:
                st.altair_chart(table_bubble, use_container_width=True)

            # Row 3
            col1, col2 = st.columns([1,4])
            with col1:
                st.altair_chart(scatter_chart, use_container_width=True)
            with col2:
                st.altair_chart(bar_negative, use_container_width=True)

            # Row 4
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                st.altair_chart(boxplot_chart_month, use_container_width=True)
            with col2:
                st.altair_chart(violin_chart)
            with col3:
                st.altair_chart(stripplot)

            # Row 5
            col1, col2 = st.columns([1,1])
            with col1:
                st.altair_chart(hexbin_chart)
            with col2:
                st.altair_chart(ridgeline_plot)

            # Row 6
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                st.altair_chart(scatter_binned, use_container_width=True)
            with col2:
                st.altair_chart(scatter_chart, use_container_width=True)
            with col3:
                st.altair_chart(scatter_loess, use_container_width=True)

            col1, col2, col3 = st.columns([1, 4, 1])

            # Data download
            col1, col2, col3 = st.columns([1, 4, 1]) 
            col2.markdown("""
                ---
                ## Data download
                """)
            # Download data preparation
            gdf = gpd.GeoDataFrame(lst_df, geometry=[shape(aoi_json)]*len(lst_df))
            csv_data = convert_df(gdf)
            geojson_data = convert_gdf(gdf)
            col2.warning('Please note, data download resets the dashboard view. This seems to be a Streamlit limitation as described in [this open issue](https://github.com/streamlit/streamlit/issues/4382).')
            # Download CSV
            with col2.container(border=True):
                cont1_1, cont1_2 = st.columns([1, 3])
                with cont1_1:
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=sub_name + "-LST.csv",
                        mime="text/csv",
                        key='download-csv'
                    )
                with cont1_2:
                    st.write('The CSV file includes the average land surface temperature value in Celsius, date and time information and the hydrological basin geometry in the WKT format.')
            # Download GeoJSON
            with col2.container(border=True):
                cont2_1, cont2_2 = st.columns([1, 3])
                with cont2_1:
                    st.download_button(
                        label="Download GeoJSON",
                        data=geojson_data,
                        file_name=sub_name + "-LST.geojson",
                        mime="application/json",
                        key='download-geojson'
                    )
                with cont2_2:
                    st.write('The GeoJSON provides the same geometry values for each feature. GeoJSON properties include the average land surface temperature value, date and time infromation.')

col1, col2, col3 = st.columns([1, 4, 1])
col2.markdown("""
    ---
    ## References
    * Hydrological basins in Europe - [FAO Map Catalog.](https://data.apps.fao.org/map/catalog/srv/api/records/1849e279-67bd-4e6f-a789-9918925a11a1)
    * Watershed Boundary Dataset in the USA - [USGS.](https://www.usgs.gov/national-hydrography/watershed-boundary-dataset)
    * Hydrological basins in Australia and New Zealand - [FAO Map Catalog.](https://data.apps.fao.org/catalog/dataset/a1a0e9ee-5062-4950-a6b9-fdd2284b2607)
    * Hydrological basins in Near East - [FAO Map Catalog.](https://data.apps.fao.org/catalog/iso/7ae00a40-642b-4637-b1d3-ffacb13360db)
    * Hydrological basins in Southeast Asia - [FAO Map Catalog.](https://data.apps.fao.org/catalog/iso/ee616dc4-3118-4d67-ba05-6e93dd3e962f)
    * Land Surface Temperature - [MODIS via Google Earth Engine.](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2)
    """)

