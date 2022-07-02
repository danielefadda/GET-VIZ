from utils import *

st.title('A Framework to maniupalate Data')

data = load_data('data/wb_example.csv')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)