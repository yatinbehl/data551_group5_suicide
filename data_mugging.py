import pandas as pd
import pycountry


def clean_data(file_path):
    data = pd.read_csv(file_path)
    filtered_data = data[['country', 'suicides_no']]
    filtered_data = filtered_data.groupby(['country']).sum().sort_values(by=['suicides_no'],
                                                                         ascending=False)
    filtered_data = filtered_data.reset_index()

    list_countries = filtered_data['country'].unique().tolist()
    country_code_dict = {}

    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            country_code = country_data[0].alpha_3
            country_code_dict.update({country: country_code})
        except:
            country_code_dict.update({country: country_code})

    country_df = pd.DataFrame.from_dict(country_code_dict, orient='index')
    country_df = country_df.reset_index()
    country_df.columns = ['country', 'code']

    filtered_data['code'] = country_df['code']

    return filtered_data


# Suicides_per capita plot:
def suicides_per_capita(suicide_data):
    # Rename the dataframe:
    suicide_subset = suicide_data
    suicide_subset['year'] = pd.to_datetime(suicide_subset['year'], format= "%Y")
    #suicide2 = suicide_subset.drop(‘country-year’, axis = 1)
    suicide_data = suicide_subset.copy()
    suicide_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k_pop','country-year','HDI','gdp_for_year','gdp_per_capita', 'generation']
    
    # Wrangling on the said dataframe:
    avg_suicides_per_capita_g = suicide_data.groupby(['country','year','age',])['suicides_per_100k_pop'].mean().reset_index()
    avg_suicides_per_capita_g.columns =['country','year','age','Average_suicides_per_capita']
    avg_suicides_per_capita_g.sort_values('Average_suicides_per_capita', ascending = False, inplace = True)
    avg_suicides_per_capita_g = avg_suicides_per_capita_g[(avg_suicides_per_capita_g['Average_suicides_per_capita']!=0)]

    return avg_suicides_per_capita_g

## AVERAGE SUICIDES by gender:
def suicides_by_gender(suicide_data):
    # Wrangling:
    # Rename the dataframe:
    #suicide_subset = suicide_data.query('year >= 1996')
    suicide_data['year'] = pd.to_datetime(suicide_data['year'], format= "%Y")
    #suicide2 = suicide_subset.drop(‘country-year’, axis = 1)
    suicide_data = suicide_data.copy()
    suicide_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k_pop','country-year','HDI','gdp_for_year','gdp_per_capita', 'generation']

    avg_suicides_per_capita = suicide_data.groupby(['year','country','sex'])['suicides_per_100k_pop'].mean().reset_index()
    #avg_suicides_per_capita.columns =['year','country','sex','Average_suicides_per_capita']
    #avg_suicides_per_capita
    avg_suicides_per_capita.columns =['year','country','sex','Average_suicides_per_capita']
    avg_suicides_per_capita.sort_values('Average_suicides_per_capita', ascending = False, inplace = True)
    group1 = avg_suicides_per_capita.groupby(['country', 'sex'])['Average_suicides_per_capita'].mean().reset_index()
    return group1

def suicide_by_gdp(suicide_data):
    suicide_data = suicide_data
    suicide_data['year'] = pd.to_datetime(suicide_data['year'], format= "%Y")
    suicide2 = suicide_data.drop('country-year', axis = 1)
    suicide_data1 = suicide2.copy()
    suicide_data1.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k_pop','HDI','gdp_for_year','gdp_per_capita', 'generation']
    x1 = suicide_data1.groupby(['country'])['suicides_no'].sum().reset_index()
    y1 = suicide_data1.groupby('country')[['gdp_per_capita','population']].mean().reset_index()
    combined11 = pd.merge(x1, y1, on='country', how='outer')
    return combined11

