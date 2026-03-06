import streamlit as st
import pandas as pd
import plotly.express as px
from plots import lifeexp_gdp_scatter
import pickle

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

    # plot
    fig = lifeexp_gdp_scatter(filtered_data_1)
    st.plotly_chart(fig, use_container_width=True)

    # === Prediction panel ===
    st.subheader("Life Expectancy Prediction")

    # load trained model
    with open("life_expectancy_model.pkl", "rb") as f:
        model = pickle.load(f)

    st.write("Enter values to estimate life expectancy using the trained Random Forest model.")

    # define ranges from dataset
    gdp_min = float(data["GDP per capita"].min())
    gdp_max = float(data["GDP per capita"].max())
    gdp_default = float(data["GDP per capita"].median())

    pov_min = float(data["headcount_ratio_upper_mid_income_povline"].min())
    pov_max = float(data["headcount_ratio_upper_mid_income_povline"].max())
    pov_default = float(data["headcount_ratio_upper_mid_income_povline"].median())

    year_min = int(data["year"].min())
    year_max = int(data["year"].max())
    year_default = int(data["year"].median())

    # input widgets
    input_gdp = st.number_input(
        "GDP per capita",
        min_value=gdp_min,
        max_value=gdp_max,
        value=gdp_default,
        step=100.0,
    )

    input_poverty = st.number_input(
        "Headcount ratio (upper middle income poverty line)",
        min_value=pov_min,
        max_value=pov_max,
        value=pov_default,
        step=0.1,
    )

    input_year = st.slider(
        "Year",
        min_value=year_min,
        max_value=year_max,
        value=year_default,
        key="prediction_year_slider",
    )

    # prediction
    if st.button("Predict Life Expectancy"):

        input_df = pd.DataFrame({
            "GDP per capita": [input_gdp],
            "headcount_ratio_upper_mid_income_povline": [input_poverty],
            "year": [input_year],
        })

    
        prediction = model.predict(input_df)[0]

        st.metric(
            "Predicted Life Expectancy (IHME)",
            f"{prediction:.2f} years"
        )

    # show relative feature importance
    importance_df = pd.DataFrame({
        "Feature": ["GDP per capita", "headcount_ratio_upper_mid_income_povline", "year"],
        "Importance": model.feature_importances_,
    })

    st.bar_chart(importance_df.set_index("Feature"))

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


