from utils import *
from chart import *
from datetime import datetime

st.set_page_config(page_title="VIZ Data", page_icon="📊", layout='wide', initial_sidebar_state='collapsed')
head()

if 'dataset_loaded' in st.session_state:
    with st.sidebar:
        if st.checkbox('Show session state'):
            'st.session_state:', st.session_state

    if st.session_state['dataset_loaded']:
        # set the initial default value of the slider widget
        dates = get_dates(st.session_state['df'], date_column=st.session_state['col_date'], freq='AS')
        dates = dates.to_frame()

        # todo: fix timeline
        # select_year = st.write('You select:', int(d.timestamp()))
        # dates['local_time'] = dates['date'].dt.tz_localize('Europe/London')
        # Timeline
        # st.altair_chart(
        #     draw_dates(
        #         dates=dates,
        #         date_col=st.session_state['col_date'],
        #         current_date=d
        #     ), use_container_width=True
        # )
        # end of Timeline
        col1, col2 = st.columns(2)
        with col1:
            d = st.selectbox(
                "Select a date to be visualized on the map",
                options=dates,
                format_func=lambda x: x.strftime("%b %Y")
            )
            st.session_state['f_df'] = st.session_state['df'][st.session_state['df']['date'] == d]
            indicator = index_selector(st.session_state['f_df'], st.session_state['col_index_name'])

            f_map = folium_map(
                geo_data='data/ne_50m_admin_countries.geojson',
                df=st.session_state['f_df'],
                indicator=indicator,
                col_index_name=st.session_state['col_index_name'],
                col_index_value=st.session_state['col_index_value'],
                col_country_code=st.session_state['col_country_code']
            )

            # st.write(
            #     calculate_data_for_legend(
            #         data=st.session_state['f_df'],
            #         col_country_name=st.session_state['col_country_name'],
            #         col_country_code=st.session_state['col_country_code']
            #     )
            # )
            # st.altair_chart(wilkinson_chart(
            #     col_country_name=st.session_state['col_country_name'],
            #     col_country_code=st.session_state['col_country_code'])
            # )
        with col2:
            countries = st.multiselect(
                'Select one or more countries to visualize their timeseries',
                options=get_country_list(st.session_state['df'], 'Country')
            )
            # st.write(countries)
            st.session_state['ts_df'] = filter_by_country(st.session_state['df'], st.session_state['col_country_name'],
                                                          countries)

            # st.write(st.session_state['ts_df'])
            ts_chart = draw_timeseries(
                data=st.session_state['ts_df'],
                col_date=st.session_state['col_date'],
                col_index_name=st.session_state['col_index_name'],
                col_index_value=st.session_state['col_index_value'],
                col_country_code=st.session_state['col_country_code'],
                current_date=d
            )

            st.altair_chart(ts_chart, use_container_width=True)
    if st.checkbox('Show raw data'):
        if st.session_state['df'].empty == False:
            st.subheader('Raw data')
            st.write(st.session_state['df'])
        else:
            st.subheader('No data loaded yet')
            st.write('You must load a well formed dataset to visualize it')




else:
    st.subheader('You have to laod a dataset before visualize it!')
    with st.sidebar:
        st.write('go to the previous page and load a dataset')
