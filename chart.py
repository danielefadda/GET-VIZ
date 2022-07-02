import altair as alt
import math, random
import streamlit as st
import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import folium_static
from streamlit_folium import st_folium

import streamlit

from utils import *


def draw_dates(dates, date_col, current_date, shape='square', area_size=100, granularity='year'):
    # todo: set this method private at the end.
    """
    This function draws the timeline on the top of the dashboard which is used as a timeframe selector and the
    click_time selector
    """
    d_width = dates.shape[0] * (math.sqrt(area_size) / 3.14 * 6)
    chart_width = d_width if d_width < 800 else 800

    if shape == 'square':
        load_data = alt.Chart(dates).mark_square(
            size=area_size
        )
    else:
        load_data = alt.Chart(dates).mark_circle(
            size=area_size
        )
    # todo: aggiungere un marker ruler se i dati sono troppi.

    time_chart = load_data.encode(
        x=alt.X(
            field=date_col,
            type='temporal',
            timeUnit=granularity,
            title=None,
            axis=alt.Axis(
                grid=False, domain=False, labelFlush=False, ticks=False, labelPadding=0
            ),
        ),
        tooltip=[alt.Text(field=date_col, type='temporal', timeUnit=granularity, title='Date')],
        color=alt.condition(f"datum.local_time=={int(current_date.timestamp())}", alt.value('red'), alt.value('gray')),
        # todo: correggere selezione colore - controllare la seguente trasformazione in timeunit.
        # color=alt.Color(field=date_col,type='temporal')
        #     .transform_timeunit(
        #     newDate=f'{self.granularity}({self.date_column})'
        # )
    ).properties(
        height=50,
        width=chart_width,
        padding={"left": 5, "top": 15, "right": 5, "bottom": 5}
    ).configure_view(
        strokeWidth=0
    )
    return time_chart


def index_selector(data, col_index_name):
    indicators = data[col_index_name].unique().tolist()
    indicator = st.selectbox(
        'select an index to be visualized on the map',
        options=indicators
    )
    return indicator


def folium_map(geo_data, df, indicator, col_index_name, col_index_value, col_country_code):
    # my_scale = (df[df[col_index_name] == indicator].quantile((0, 0.1, 0.75, 0.9, 0.98, 1)))[col_index_value].tolist()
    gdf = read_geofiles(geo_data)
    # Initiate a folium map
    # gdf_m = gdf.merge(df[['FIPS','Country','value']], on="FIPS")
    m = folium.Map(location=[40, 10], width='90%', zoom_start=2, tiles=None)
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(m)
    # Plot Choropleth map using folium
    folium.Choropleth(
        geo_data=gdf,  # This is the geojson file for the Unite States
        name='Titolo da definire',
        data=df[df[col_index_name] == indicator],  # This is the dataframe we created in the data preparation step
        columns=[col_country_code, col_index_value],
        # 'state code' and 'metrics' are the two columns in the dataframe that we use to grab the median sales price
        # for each state and plot it in the choropleth map
        key_on='feature.properties.adm0_a3',
        # This is the key in the geojson file that we use to grab the geometries for each state in order to add the
        # geographical boundary layers to the map
        fill_color='BuPu',
        # threshold_scale=my_scale,
        nan_fill_color="White",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=indicator,
        highlight=True,
        line_color='black',
        smooth_factor=1).geojson.add_to(m)
    folium_static(m)
    # st_folium(m, key="init", width=1000, height=600)


def draw_timeseries(data, col_date, col_index_name, col_index_value, col_country_code, current_date):
    base = alt.Chart(
        data
    ).mark_line(
        interpolate='monotone',
        tooltip=True,
        point=True
    ).encode(
        x=alt.X(field=col_date, type='temporal', title=None, axis=alt.Axis(gridColor="white")),
        color=alt.Color(f'{col_country_code}:N', title='Countries')

    )
    print('current_datecurrent_datecurrent_date', current_date)

    time_ruler = alt.Chart(
        pd.DataFrame({'x': [current_date], 'legend':['time on the map']})
    ).mark_rule(
        strokeWidth=5,
        opacity=0.2,
        color='black'
    ).encode(
        x=alt.X('x:T', title=None),
    )

    idx = data[col_index_name].unique().tolist()

    charts = []
    for el in idx:
        charts.append(
            alt.layer(
                time_ruler +
                base.transform_filter(
                f"datum.{col_index_name}== '{el}'"
            ).encode(
                y=alt.Y(f'{col_index_value}:Q', title=None,
                        scale=alt.Scale(zero=False)
                        ),
                tooltip=[alt.Text(field=col_index_value, type='quantitative', title=f'{el}')],
            ).properties(
                height=250,
                width=530,
                title=el
            )
                      )
        )

    allCharts = alt.vconcat(*charts).resolve_scale(y='independent')
    return allCharts

#
# def calculate_data_for_legend(data, col_country_code, col_country_name, columns=12):
#     data_legend = gpd.read_file('data/world_countries_geo.geojson')
#     data_legend = data_legend.sort_values(by=['Sub-region Name', 'FIPS']).dropna()
#
#     codes = data[col_country_code].unique()
#     names = data[col_country_name].unique()
#     zip_iterator = zip(codes, names)
#     code_dicts = dict(zip_iterator)
#     print(code_dicts)
#
#     # self.domain_names = codes
#     # self.range_names = self.generate_array_of_colors(len(codes))
#     # self.scale = alt.Scale(domain=self.domain_names, range=self.range_names)
#     #
#     # self.set_colors(len(codes))
#
#     data_legend = data_legend[['name', col_country_code, 'Sub-region Name', 'Region Name']].sort_values(
#         ['Region Name', 'Sub-region Name', col_country_code])
#     data_legend = data_legend[data_legend[col_country_code].isin(list(codes))]
#
#     data_legend['RN'] = data_legend.groupby('Sub-region Name').cumcount() + 1
#     data_legend.rename(columns={'name': col_country_name, col_country_code: col_country_code}, inplace=True)
#     data_legend['Sub-region Name ordered'] = ""
#
#     for index, row in data_legend.iterrows():
#         c = columns  # scegliere il numero di colonne da visualizzare su una riga:
#         r = math.floor(row['RN'] / c)
#         data_legend.at[index, 'Sub-region Name ordered'] = row[
#             'Sub-region Name'] if r == 0 else f"{row['Sub-region Name']} -{str(r + 1)}"
#
#     c_names = list(data_legend['Sub-region Name ordered'].unique())
#     labels_list = []
#     import re
#     for el in c_names:
#         if len(re.findall(r"\b -\d", el)) > 0:
#             el = ''
#         labels_list.append(el)
#
#     return data_legend, labels_list
#
#
# def wilkinson_chart(col_country_code, col_country_name, ):
#     # self.click_country = self.selector_country()
#
#     data_legend, labels_list = calculate_data_for_legend(
#         data=st.session_state['f_df'],
#         col_country_code=st.session_state['col_country_code'],
#         col_country_name=st.session_state['col_country_code'],
#         columns=12)
#
#     base_legend = alt.Chart(
#         data_legend
#     ).transform_window(
#         id='rank()',
#         groupby=['Sub-region Name ordered']
#     )

    # rect_legend = base_legend.mark_rect(
    #     stroke='white',
    #     color='lightgray',
    #     height=14
    # ).encode(
    #     x=alt.X('id:O', title=None, axis=None),
    #     y=alt.Y('Sub-region Name ordered:N', title=None,
    #             sort=alt.EncodingSortField(field='Region Name', order='ascending')),
    #     # color=alt.condition(self.click_country, alt.Color(f'{col_country_code}:N', scale=self.scale),
    #     #                     alt.value('lightgray'))
    #     # legend=alt.Legend(orient='bottom')
    # ).properties(width={"step": 18}, height={"step": 15})
    #
    # text_legend = base_legend.mark_text(
    #     fontSize=8,
    #     cursor='pointer'
    # ).transform_calculate(
    #     label=f'substring(datum.{col_country_code}, 0, 2)'
    # ).encode(
    #     x=alt.X('id:O', title=None, axis=None),
    #     y=alt.Y('Sub-region Name ordered:N', title=None,
    #             sort=alt.EncodingSortField(field='Region Name', order='ascending'),
    #             axis=alt.Axis(values=labels_list, domain=False)),
    #     text='label:N',
    #     # color=alt.condition(self.click_country, alt.value('white'), alt.value('#484848')),
    #     tooltip=[alt.Tooltip(f'{col_country_name}:N', title='Country')]
    # ).properties(width={"step": 18}).add_selection(
    #     alt.selection_single())  # selection used as a workaround for a bug on tooltips
    #
    # country_selector = (rect_legend + text_legend).facet(
    #     row=alt.Row(
    #         'Region Name:N',
    #         header=alt.Header(labelOrient='left'),
    #         # title=None,
    #
    #         title=f"Select a Country to visualize indicators over time",
    #     )
    # ).resolve_scale(
    #     y='independent'
    # ).properties(
    #     spacing=5
    # )
    #
    # return country_selector
