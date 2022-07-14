from utils import *


st.set_page_config(page_title="Wrangling Data", page_icon="🌍")

head()
with st.sidebar:
    ## Init session_state
    if 'dataset_loaded' not in st.session_state:
        st.session_state['dataset_loaded'] = False

    'st.session_state:', st.session_state
    clear_state_button = st.button('clear all')
    if clear_state_button:
        st.session_state['dataset_loaded'] = False
        try:
            field1.empty()
        except:
            pass

load_option = st.selectbox(
    'How would you load your data?',
    ('From your pc', 'Use an example dataset',  'Explore the World Bank dataset'))

if load_option == 'From your pc':
    st.session_state['dataset_loaded'] = False
    st.session_state['df'] = load_local_data()
    expander = st.expander("See explanation")
    st.write("""
    Get the data using a personal csv file. It is necessary to have a set of data in tidy format.
    
    There are three rules which make a dataset tidy:
    - Each variable must have its own column.
    - Each observation must have its own row.
    - Each value must have its own cell.
    """)

if load_option == 'Use an example dataset':
    st.session_state['dataset_loaded'] = False
    examples_list = st.selectbox(
        'Choose a dataset:',
        ('wb_example', 'country-codes'))
    load_data_button = st.button('Load data')
    if load_data_button:
        st.session_state['dataset_loaded'] = True
        data = load_data(f'data/{examples_list}.csv')
        st.session_state['df'] = data
        st.write(data.head())
        get_columns_name(data)

if load_option == 'Explore the World Bank dataset':
    st.session_state['dataset_loaded'] = False
    st.markdown(f"<h5>{load_option}</h5>", unsafe_allow_html=True)
    with st.expander('Change dataset', expanded=True):
        st.markdown(
            "<em>You can choose two indicators from the World Bank dataset. The first one is represented on the map and "
            "it's mandatory, the second one is optional.</em>", unsafe_allow_html=True)
        st.markdown('---')
        st.markdown('<h5>Map indicator</h5>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input('You can filter the World Bank datasets using a keyword:', '', key=7890)
            df = get_wb_indicators_list(query=query)
        with col2:
            st.metric(label='Number of datasets', value=df.shape[0])
        if df.shape[0] > 0:
            map_indicator = st.selectbox(
                label="Map indicator:",
                options=df['value'])
            id_map = df['id'][df['value'] == map_indicator].iloc[0]
        else:
            st.error(f"We can't find any dataset using the query '{query}'")
        st.markdown('<h5>Secondary indicator</h5>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            query2 = st.text_input('You can filter the World Bank datasets using a keyword:', '', key=123456)
            df2 = get_wb_indicators_list(query=query2)
        with col2:
            st.metric(label='Number of datasets', value=df2.shape[0])
        if df2.shape[0] > 0:
            sec_indicator = st.selectbox(
                label=f'Secondary indicator:',
                options=df2['value']
            )
            id_sec = df2['id'][df2['value'] == sec_indicator].iloc[0]
        else:
            st.error(f"We can't find any dataset using the query '{query2}'")
        time_values = st.slider(
            'Select a range of dates',
            1960, 2022, (2000, 2020))
        st.write('Values:', time_values)
    st.markdown(
        f"The indicator to visualize on the map is: <strong>{id_map}</strong>.</br>"
        f"The secondary indicator is: <strong>{id_sec}</strong>",
        unsafe_allow_html=True)
    if st.button('Get the data'):
        dataframe = world_bank(map_index=id_map, range_values=time_values, second_index=id_sec)
        st.session_state['dataset_loaded'] = True
        st.session_state['df'] = dataframe
        st.write(dataframe.head())


footer()
