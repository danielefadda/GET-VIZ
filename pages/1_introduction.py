import streamlit as st

st.set_page_config(page_title="Introduction", page_icon="📈")

st.write("# Welcome to GET-Viz! 👋")

st.markdown(
    """
    ### GET-Viz is an opensource library for the automatic generation of visual dashboard for geographical time series 

    GET-Viz, an open-source python library that implements a dashboard for visual exploration of social and economic 
    indicators.The dashboard allows the user to interactively explore multiple dimensions of 
    the data. In particular, GET-Viz proposes two main filtering dimensions: temporal, to select a specific time 
    instant; spatial, to select multiple countries. The selections can be combined to implement a comparative 
    exploration of the resulting time series. The dashboard shows the evolution of one or multiple indexes to be 
    analyzed. 
    
    #### Get the data using a set of predefined connectors
    World Bank is available at the moment, but we are planning to extend the work to the most famous API Connectors, such as:  WHO (https://www.who.int/data), OECD (https://data.oecd.org/), UN (https://data.un.org/). You can contact us if you want to help.
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

    ### Introduction
    
    The effective graphical presentation of information is an essential skill in most scientific disciplines. 
    Visualization is intended to clearly describe and communicate information through graphic means, 
    allowing everyone to understand the data more explicitly [1]. Through visualization, the results of data 
    processing are made more accessible, simple, and user-friendly [2], facilitating the understanding of information 
    to those who have no specific technical or domain knowledge [3]. A proper way to graphically describe a complex 
    phenomenon is through the use of dashboards. As stated in [4], “compared to visualization modalities for 
    presentation and exploration, dashboards bring together challenges of at-a-glance reading, coordinated views, 
    tracking data and both private and shared awareness”. The access to complex phenomena is made possible through 
    the realization of multiple linked displays [5], where sub-dimensions of the whole data are shown in detail and 
    the interaction on one display propagates selection and filtering to the other’s views. Thus, the complexity of 
    the data to explore is mitigated through the use of interaction with the observer. 

    
    **👈 Select a demo from the dropdown on the left** to see some examples
    of what Streamlit can do!

    ### Want to learn more?

    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
      forums](https://discuss.streamlit.io)

    ### See more complex demos

    - Use a neural net to [analyze the Udacity Self-driving Car Image
      Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
