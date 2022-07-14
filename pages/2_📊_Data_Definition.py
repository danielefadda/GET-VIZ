from utils import *

st.set_page_config(page_title="VIZ Data", page_icon="📊")
head()
st.title('Data definition')
# 'st.session_state:', st.session_state
if 'dataset_loaded' in st.session_state:
    if st.session_state['df'].empty == False:
        if st.checkbox('show raw data'):
            st.write(st.session_state['df'])
        get_columns_name(st.session_state['df'])
    else:
        st.subheader('No data loaded yet')
        st.write('You must load a well formed dataset to visualize it')



else:
    st.subheader('You have to laod a dataset before defining attributes!')
    with st.sidebar:
        st.write('go to the previous page and load a dataset')
