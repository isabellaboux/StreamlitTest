import plotly.express as px


def lifeexp_gdp_scatter(df):
    fig = px.scatter(
        df,
        x="GDP per capita",
        y="Life Expectancy (IHME)",
        size="Population",
        color="country",
        hover_name="country",
        hover_data={
            "year": True,
            "GDP per capita": ":.2f",
            "Life Expectancy (IHME)": ":.2f",
            "Population": ":,.0f",
        },
        log_x=True,
        title="GDP per Capita vs Life Expectancy",
        labels={
            "GDP per capita": "GDP per capita (log scale)",
            "Life Expectancy (IHME)": "Life Expectancy (IHME)",
            "Population": "Population",
            "country": "Country",
        },
    )

    return fig