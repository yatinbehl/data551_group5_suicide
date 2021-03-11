import plotly.express as px
import altair as alt
from altair import datum
#from vega_datasets import data
#import pylab as plt
import pandas as pd

# The required world map code:
def create_world_plot(data, location, color, hover_name):
    fig_map = px.choropleth(data,
                            locations=location,
                            color=color,
                            hover_name=hover_name,
                            color_continuous_scale=px.colors.diverging.Earth,
                            width=200, height=262)

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width=700,
        #paper_bgcolor="Black",
        geo=dict(bgcolor='rgba(50,50,50,50)'),
        paper_bgcolor='#313131',
        #legend = dict( font = dict(size =12, color = 'balck'),
        legend_title="Legend Title",
        font=dict(
        #family="Courier New, monospace",
        size=11,
        color="white"))

    return fig_map

# The box plot that shows the variations across generations:
def plot_suicide_boxplot(country_dropdown, data):
        data_country_filter = data[data['country'] == country_dropdown]
        alt.themes.enable('dark')
        chart = alt.Chart(data_country_filter).mark_boxplot().encode(
            alt.X('suicides/100k pop', title='Suicides per 100k'),
            alt.Y('generation', title = None),
            fill = alt.Color('generation', legend=None, scale= alt.Scale(scheme= 'blueorange'))
            ).facet(alt.Row('sex', title = None),title='Suicides_per_100K Population vs Generation').properties(columns = 1).interactive().configure_axis(labelFontSize=10)
        return chart.to_html()

# Aditya's plot:
def plot_suicide_gdp(data, sex, country, age, year):
    alt.themes.enable('dark')
    df = data[data['country'] == country]
    #for gender in sex:
    #if type(sex) == 'str':
        #df = df[df['sex'] == sex]
    if not type(sex) == list:
        df = df[df['sex'] == sex]
    else:
        pass
    df = df[df['age'] == age]
    # df = df[df['generation'] == generation]
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    year = pd.to_datetime(year, format= '%Y')
    print(year[0])
    print(year[1])
    df = df[df['year'] > year[0]]
    df = df[df['year'] < year[1]]

    chart = alt.Chart(df, title = 'Suicide Trends per Country').mark_circle(color = 'yellow').encode(
        alt.X('year', title='Year'),
        alt.Y('suicides_no', title='Total Number of Suicides'),
        alt.Color('sex', scale= alt.Scale(scheme= 'blueorange')),
        alt.Size('gdp_per_capita ($):Q', legend = None),tooltip = [alt.Tooltip('country:N'), alt.Tooltip('gdp_per_capita ($):Q')]).interactive().configure_axis(grid = False)
    return chart.to_html()

# Poojitha's plot:
# Suicide per capita data plot:
def age_plot(country_dropdown, source, year):
    alt.themes.enable('dark')
    data = source
    data = data[data['country'] == country_dropdown]

    data['year'] = pd.to_datetime(data['year'], format='%Y')

    year = pd.to_datetime(year, format= '%Y')
    print(year[0])
    print(year[1])
    #data = data_country_filter[data_country_filter['country'] == country_dropdown]
    data = data[data['year'] > year[0]]
    data = data[data['year'] < year[1]]
    #print(data.head())

    brush = alt.selection_interval()
    click = alt.selection_multi(fields = ['age'], bind = 'legend')
    points = (alt.Chart(data, title = 'Mean Suicides per Capita').mark_line(size = 7).encode(
    x = 'year',
    y = 'Average_suicides_per_capita',
    color = alt.condition(brush, 'age', alt.value('lightgray'),scale= alt.Scale(scheme= 'blueorange')),
    opacity = alt.condition(click, alt.value(0.9), alt.value(0.2))).add_selection(brush)).configure_axis(grid = False)
    points.configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=2,
    cornerRadius=2,
    orient='bottom')
    plot = points.add_selection(click)
    return plot.to_html()

# Suicide variations for the gender:
def suicides_gender(source):
    group1 = source
    click = alt.selection_multi()
    alt.data_transformers.disable_max_rows()
    color_scale = alt.Scale(domain=['male', 'female'],
                            range=['#5389b8', '#c87e35'])


    left = (alt.Chart(group1).transform_filter(
        (datum.sex == 'female')
    ).encode(
        y=alt.Y('country', axis=None),
        x=alt.X('Average_suicides_per_capita',
                title='Average_suicides_per_capita',
               sort = alt.SortOrder('descending'),
               axis = alt.Axis(orient = 'top'),
               scale=alt.Scale(domain=(0, 70))),
        color=alt.Color('sex:N', scale=color_scale, legend=None),
        opacity=alt.condition(click, alt.value(1.0), alt.value(0.5)),
        tooltip = [alt.Tooltip('country:N'), alt.Tooltip('Average_suicides_per_capita:Q')],
    ).mark_bar().properties(title='Female').add_selection(click))

    middle = alt.Chart(group1).encode(
        y=alt.Y('country', axis=None),
        text=alt.Text('country'),
    ).mark_text(color = 'white').properties(width=150)

    right = (alt.Chart(group1).transform_filter(
        (datum.sex == 'male')
    ).encode(
        y=alt.Y('country', axis=None),
        x=alt.X('Average_suicides_per_capita', title='Average_suicides_per_capita',axis = alt.Axis(orient = 'top'),scale=alt.Scale(domain=(0, 70))),
        color=alt.Color('sex:N', scale=color_scale, legend=None),
        opacity=alt.condition(click, alt.value(1.0), alt.value(0.5)),
        tooltip = [alt.Tooltip('country:N'), alt.Tooltip('Average_suicides_per_capita:Q'), alt.Tooltip('sex')],
    ).mark_bar().properties(title='Male').add_selection(click))

    chartf = alt.concat(left, middle, right, spacing=4).configure_axis(grid = False)
    return chartf.to_html()

def country_plot(source):
    alt.themes.enable('dark')
    combined11 = source
    selection = alt.selection_single()
    country_chart = alt.Chart(combined11, title = 'Spread of Countries - GDP Vs Total Suicide Numbers').mark_point(filled = True).encode(
    alt.X('gdp_per_capita:Q'),
    alt.Y('suicides_no'),
    alt.Size('population:Q', scale = alt.Scale(range=[0,2000]), legend = None),
    alt.Order('population:Q', sort = 'ascending'),
    tooltip = [alt.Tooltip('country:N'),
               alt.Tooltip('suicides_no:Q'),
               alt.Tooltip('gdp_per_capita:Q'),
               alt.Tooltip('population')
              ],
    color = alt.condition(selection,'country', alt.value('darkgrey'), scale= alt.Scale(scheme= 'blueorange'),legend = None)).add_selection(selection).configure_axis(grid = False)
    return country_chart.to_html()