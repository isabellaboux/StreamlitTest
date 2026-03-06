import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Worldwide Analysis of Quality of Life and Economic Factors")
st.write("This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years.\n\nUse the panels to select options and interact with the data.")

tab_GO, tab_CDD, tab_DE = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])     

# get data
data_url = 'https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv'
data = pd.read_csv(data_url)
data.head()

with tab_GO:
    
    # Year range slider
    min_year = data["year"].min()
    max_year = data["year"].max()

    selected_years_1 = st.slider(
        "Select year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key="year_slider_tab_GO",
    )
    
    # filter data based on user input
    filtered_data_1 = data[
        (data["year"] >= selected_years_1[0]) &
        (data["year"] <= selected_years_1[1])
    ]

    # add metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("mean of life expectancy", str(filtered_data_1["Life Expectancy (IHME)"].mean().round(2)))
    col2.metric("median of GDP per capita", str(filtered_data_1["GDP per capita"].median().round(2)))
    col3.metric("mean of headcount_ratio_upper_mid_income_povline", str(filtered_data_1["headcount_ratio_upper_mid_income_povline"].mean().round(2)))
    col4.metric("Number of countries", str(filtered_data_1["country"].nunique()))

    # add plot
    # fig = px.scatter(
    #     filtered_data_1,
    #     x="gdpPercap",
    #     y="lifeExp",
    #     color="continent",
    #     hover_name="country"
    # )

    # st.plotly_chart(fig, use_container_width=True)

with tab_DE:

    # create a country multiselector
    countries = sorted(data["country"].unique())
    selected_countries = st.multiselect(
        "Select country names",
        options=countries,
        default=countries[:3]
        )
    
    # Year range slider
    min_year = data["year"].min()
    max_year = data["year"].max()

    selected_years_2 = st.slider(
        "Select year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        
    )
    

    # filter data based on user input
    filtered_data = data[
        (data["year"] >= selected_years_2[0]) &
        (data["year"] <= selected_years_2[1])
    ]
    if selected_countries:
        filtered_data = filtered_data[filtered_data["country"].isin(selected_countries)]


    # display dataframe
    st.dataframe(filtered_data)


    

fig = px.scatter(
    filtered_data_1,
    x="gdpPercap",
    y="lifeExp",
    color="continent",
    hover_name="country"
)

st.plotly_chart(fig, use_container_width=True)