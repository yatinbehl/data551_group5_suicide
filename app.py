import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
#import dash_daq as daq

import dash_plots


from data_mugging import clean_data
import data_mugging
import pandas as pd

suicide_dataset = pd.read_csv('master.csv')
cleaned_data = clean_data('master.csv')


figure1 = global_suicide_stat = dash_plots.create_world_plot(cleaned_data,
                                                   location='code',
                                                   color='suicides_no',
                                                   hover_name='country')

# Suicides_per_capita plot:
data_clean_suicide_per_capita = data_mugging.suicides_per_capita(
    suicide_dataset)

# Suicides by gender plot:
data_suicides_by_gender = data_mugging.suicides_by_gender(suicide_dataset)

# suicides by gdp
data_suicides_by_gdp = data_mugging.suicide_by_gdp(suicide_dataset)

# Create a list that is required for the slider:
suicide_dataset['year'] = pd.to_datetime(suicide_dataset.year, format='%Y')
suicide_dataset['year'] = suicide_dataset['year'].dt.year
date_list = suicide_dataset['year'].unique().tolist()
date_label = [str(i) for i in date_list]
zipobj = zip(date_label, date_label)
dic_date = dict(zipobj)
# dict_date_hard_code = {i : '{}'.format(i) for i in range(1987,2016, 3)}

# Create an array for year:
year_value = [1985, 2016]
year_value = pd.to_datetime(pd.Series(year_value), format='%Y')
year_value = year_value.dt.year

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

app.layout = dbc.Container([
    html.H1('SUICIDES : A GLOBAL IMPERATIVE',
            style={'text-align': 'center'}),
    html.H5('Description : The Dashboard provides an in depth analysis of all factors related to the Number of Suicides in countries across the world'),
    html.Br(),
    html.Div(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    'COUNTRY',
                    dcc.Dropdown(
                    id='country-dropdown',
                    value='Canada',
                    options=[{'label': col, 'value': col} for col in cleaned_data['country']],placeholder = 'Select Country'),

                html.Br(),
                'AGE',
                dcc.Dropdown(
                id='age-dropdown',
                value='15-24 years',
                options=[{'label': col, 'value': col} for col in suicide_dataset['age'].unique()]),

                html.Br(),

                'GENDER',
                dcc.Dropdown(
                id='gender-dropdown',
                value='male',
                options=[{'label': 'Male', 'value': 'male'},
                         {'label': 'Female', 'value': 'female'}],
                # multi = True
                # labelStyle={'display': 'inline-block', 'cursor': 'pointer', 'margin-left': '20px'}
                )])]))], width=4),

                dbc.Col(
                    [dbc.Card(dbc.CardBody([html.P(dcc.Graph(figure=figure1))]))], width=8),
            ]
        ),
        html.Br(),

        html.H3('Suicide Trends per Country'),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    dbc.Row([
                        dbc.Col([
                            # Aditya's graph:
                            html.Iframe(
                                id='scatter',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'})
                                ]),
                        dbc.Col([
                            html.Iframe(
                                srcDoc=dash_plots.country_plot(
                                    source=data_suicides_by_gdp),
                                id='scroll-plot',
                                style={'border-width': '0',
                                    'width': '100%', 'height': '410px'}
                            )
                                ])
                                ]),
                                ])
                                ]))], width=12)
            ]),
        html.Br(),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                     html.Div(
                                    dcc.RangeSlider(
                                    id='range-slider',
                                    min=min(date_list),
                                    max=max(date_list),
                                    step=10,
                                    value=[min(date_list), max(date_list)],
                                    marks=dic_date,
                                    included=False
                                    )
                     ),
                    # html.Div(id='text-space')
                ])
                ]
                )
                )
                ]
                )
            ]
        ),


        html.H3('Other Factors'),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    dbc.Row([
                        dbc.Col([
                            html.Iframe(
                                srcDoc=dash_plots.age_plot(
                                    country_dropdown='Canada', source=data_clean_suicide_per_capita, year=[1985, 2016]),
                                id='mark_point',
                                style={'border-width': '0',
                                    'width': '100%', 'height': '400px'}
                                 )
                        ]),
                        dbc.Col([
                            html.Iframe(
                                srcDoc=dash_plots.plot_suicide_boxplot(
                                    country_dropdown='Canada', data=suicide_dataset),
                                id='boxplot',
                                style={'border-width': '0',
                                    'width': '100%', 'height': '400px'}
                            ),
                        ])
                        ])])]))], width=12)]),
        html.Br(),

        html.H3('Mean Number of Suicides by Gender - All Countries'),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    html.Iframe(
                                srcDoc=dash_plots.suicides_gender(
                                    data_suicides_by_gender),
                                id='twinbar',
                                style={'border-width': '0',
                                    'width': '120%', 'height': '400px'}
                            ),
                ])]))

                ])
            ]
        )])])

# Sowmya's graph
@ app.callback(
    Output('boxplot', 'srcDoc'),
    # Output('barplot', 'srcDoc'),
    [Input('country-dropdown', 'value')])
def update_output(chosencountry):
    return dash_plots.plot_suicide_boxplot(chosencountry, data=suicide_dataset)

# Aditya's graph
@ app.callback(
    Output('scatter', 'srcDoc'),
    Input('gender-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    # Input('generation-dropdown', 'value'),
    Input('range-slider', 'value')
)
def update_output2(gender, country, age, year):
    return dash_plots.plot_suicide_gdp(data=suicide_dataset, sex=gender, country=country, age=age, year=year)

# Poojitha's point graph:
@ app.callback(
    Output('mark_point', 'srcDoc'),
    Input('country-dropdown', 'value'),
    Input('range-slider', 'value')
)
def update_output4(chosencountry, year):
    return dash_plots.age_plot(country_dropdown=chosencountry, source=data_clean_suicide_per_capita, year=year)

# Create a call back for the slider:
#@ app.callback(
#    Output('text-space', 'children'),
#    Input('range-slider', 'value')
#)
#def update_output5(input_value):
#    year_input=pd.to_datetime(pd.Series(input_value), format='%Y')
#    year_input=year_input.dt.year
#    return year_input


if __name__ == '__main__':
    app.run_server(debug=True)
