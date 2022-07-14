import streamlit as st

st.set_page_config(
    page_title="Get-Viz",
    page_icon="👋",
)

st.write("# Welcome to GET-Viz! 👋")

st.sidebar.success("Select a Library Functionality above.")

st.markdown("""### GET-Viz is an opensource library for the automatic generation of visual dashboard for geographical time series""")

st.info('Go to the ⬇️ **Data Loading** page to select a demo dataset, load your data or use an API connector')
st.markdown(
    """
    GET-Viz, an open-source python library that implements a dashboard for visual exploration of social and economic 
    indicators.The dashboard allows the user to interactively explore multiple dimensions of 
    the data. In particular, GET-Viz proposes two main filtering dimensions: temporal, to select a specific time 
    instant; spatial, to select multiple countries. The selections can be combined to implement a comparative 
    exploration of the resulting time series. The dashboard shows the evolution of one or multiple indexes to be 
    analyzed. 

    #### Get the data using a set of predefined connectors
    [World Bank](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation) Api  are available at the moment, but we are planning to extend the work to the most famous API Connectors, such as:  [WHO](https://www.who.int/data), [OECD](https://data.oecd.org/), [UN](https://data.un.org/). You can contact us if you want to help.
    #### Load your own data
    Get the data using a personal csv file. It is necessary to have a set of data in tidy format. There are three rules which  make a dataset tidy: 

    1. Each variable must have its own column. 
    2. Each observation must have its own row. 
    3. Each value must have its own cell. Internally Get-Viz transforms data using Pandas and Geopandas to provide data in the desired format to be visualized by the library. 

    ### References

    - [1] Lee, M. D., Butavicius, M. A., Reilly, R. E.: Visualizations of binary data: A comparative evaluation. International Journal of Human-Computer Studies,  59.5, 569-602 (2003).
    - [2] Tao, F., Qi, Q., Liu, A., Kusiak, A.: Data-driven smart manufacturing. Journal of Manufacturing Systems 48, 157–169 (2018)
    - [3] Gabrielli, L., Rossi, M., Giannotti, F., Fadda, D., Rinzivillo, S.: Mobility Atlas Booklet: an urban dashboard design and implementation. ISPRS Annals of Photogrammetry, Remote Sensing and Spatial Information Sciences, 4 (2018).
    - [4] Sarikaya, A., Correll, M., Bartram, L., Tory, M., Fisher, D.: What Do We Talk About When We Talk About Dashboards?. IEEE transactions on visualization and computer graphics, 25(1), 682-692 (2019).
    - [5] Andrienko, Gennady and Andrienko, N.: Exploring spatial data with dominant attribute map and parallel coordinates. Computers, Environment and Urban Systems, 25(1), (2019)	
 

    <hr>
    👈  Go to the <strong>data loading page</strong> to select a demo dataset, load your data or use an API connector
""", unsafe_allow_html=True
)
