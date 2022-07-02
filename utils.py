import streamlit as st
import pandas as pd
import wbgapi as wb
import altair as alt
import geopandas as gpd


## Data loaders functions
@st.cache()
def load_data(file):
    return pd.read_csv(file)

@st.cache
def read_geofiles(path):
    return gpd.read_file(path)

def get_columns_name(df):
    col_list = df.columns.to_list()
    st.markdown(f"<h5>Assign columns to specific attributes</h5>", unsafe_allow_html=True)
    with st.form(key='choose_columns'):
        col1, col2 = st.columns(2)
        with col1:
            date_time_col = st.selectbox(
                'Select the date',
                col_list)
            st.session_state['col_date'] = date_time_col
        with col2:
            col_country_name = st.selectbox(
                'Select the country name',
                col_list)
            st.session_state['col_country_name'] = col_country_name
        col3, col4, col5 = st.columns(3)
        with col3:
            country_code_col = st.selectbox(
                'Select the country code',
                col_list)
            st.session_state['col_country_code'] = country_code_col
        with col4:
            index_name_col = st.selectbox(
                'Select the index name',
                col_list)
            st.session_state['col_index_name'] = index_name_col
        with col5:
            index_value_col = st.selectbox(
                'Select the index value',
                col_list)
            st.session_state['col_index_value'] = index_value_col
        st.form_submit_button(label='Submit')
    st.markdown(
        f'''
        You have selected:
        - the column <strong>{st.session_state['col_date']}</strong> for dates, 
        - the column <strong>{st.session_state['col_country_name']}</strong> for countries,
        - the column <strong>{st.session_state['col_country_code']}</strong> for country codes,
        - the column <strong>{st.session_state['col_index_name']}</strong> for index name,
        - the column <strong>{st.session_state['col_index_value']}</strong> for index value
        ''',
        unsafe_allow_html=True)
    st.markdown('''[Go to the viz section](/viz)''')

@st.cache
def get_dates(data, date_column='col_date', freq='AS'):
    dates = data.groupby(by=pd.Grouper(key=date_column, freq=freq)).first().reset_index()
    dates = dates[date_column]
    return dates

def load_local_data():
    st.markdown(f"<h5>Select a data source</h5>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your experiment results to create the dashboard")
    if uploaded_file is not None:
        dataframe = load_data(uploaded_file)
        st.write(dataframe.head())
        st.session_state['df'] = dataframe
        st.session_state['dataset_loaded'] = True
        return dataframe


## WB Utility
@st.cache
def get_wb_indicators_list(query=''):
    df = pd.DataFrame(wb.series.list(q=query))
    return df


@st.cache
def world_bank(wbIndex=None, map_index='SP.POP.TOTL', second_index='NY.GDP.PCAP.CD', startYear: int = 2000,
               endYear: int = 2020, range_values=(2000, 2020), fillNa=False):
    if wbIndex is None:
        wbIndex = [map_index, second_index]
    if len(wbIndex) < 2:
        # add one empty index if len<2 to format DF always in the same manner
        wbIndex.insert(0, '')
    startYear = range_values[0]
    endYear = range_values[1]

    # call World Bank API
    wb_data = wb.data.DataFrame(wbIndex, time=range(startYear, endYear), labels=True).reset_index()
    if fillNa:
        wb_data.iloc[:, 3:] = wb_data.iloc[:, 3:].ffill(axis=1)

    series = list(wb_data['series'].unique())
    print('series####################', series)

    c_codes = pd.read_csv('data/country-codes.csv')
    # Get data in Tiny form and prepare it to be joined with geojson data
    wb_data = pd.merge(wb_data, c_codes[['ISO3166-1-Alpha-3', 'FIPS']], left_on='economy',
                       right_on='ISO3166-1-Alpha-3', how='left').drop(columns=['economy'])

    wb_data = pd.melt(wb_data, id_vars=['FIPS','ISO3166-1-Alpha-3',  'Country', 'Series', 'series'], var_name='date')
    wb_data = wb_data[wb_data['FIPS'].notna()]

    # remove 'YR' from column name and convert string value to integer
    wb_data['date'] = wb_data['date'].str.lstrip('YR').astype(int)
    wb_data['date'] = pd.to_datetime(wb_data['date'], format='%Y')
    wb_data = wb_data.sort_values(by=['FIPS', 'date'])

    return wb_data


## END of WB Utility

@st.cache
def get_dates(data, date_column='date', freq='AS'):
    dates = data.groupby(by=pd.Grouper(key=date_column, freq=freq)).first().reset_index()
    dates = dates[date_column]
    return dates


@st.cache()
def filter_by_year(data, date_column):
    df = data[data[date_column] == selected_year]
    return df


@st.cache()
def filter_by_country(data, country_column, countries=['Belgium']):
    # df = data[data[country_column] == countries]
    df = data[data[country_column].isin(countries)]
    return df


def get_country_list(df, c_column):
    c_list = df[c_column].unique()
    return c_list


### Streamlit Layout
def head():
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: -35px;'>
        Get-Viz
        </h1>
    """, unsafe_allow_html=True
                )
    st.caption("""
        <h3 style='text-align: center;  margin-bottom: -10px;'>
        A library for the automatic generation of visual dashboard for geographical time series 
        </h3>
        <p style='text-align: center'>
        by 
    <a href='https://kdd.isti.cnr.it/people/fadda-daniele'>Daniele Fadda</a>, 
    <a href='https://kdd.isti.cnr.it/people/rinzivillo-salvatore'>Salvo Rinzivillo</a>, 
    <a href='https://kdd.isti.cnr.it/people/natilli-michela'>Michela Natilli</a>
        </p>
        <hr>
    """, unsafe_allow_html=True
               )
    # Hide Altair menu in streamlit
    st.markdown("""
        <style type='text/css'>
            details {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)



def footer():
    st.markdown("---")
    st.caption("Support us by buying a coffee!")
    st.markdown("""
        <a href="https://www.buymeacoffee.com/geoclid" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png"
            width="136"
            height="36"
            alt="Buy Me A Coffee">
        </a>
    """, unsafe_allow_html=True)

# def report():
#     pass
