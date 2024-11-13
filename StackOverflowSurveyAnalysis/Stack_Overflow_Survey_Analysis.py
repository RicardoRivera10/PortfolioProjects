import pandas as pd
import numpy as np

schema_df = pd.read_csv('Python/SQL/Data_Analysis/survey_results_schema.csv', index_col='qname')
# 'qname',usecols=['question']
raw_survey_df = pd.read_csv('Python/SQL/Data_Analysis/survey_results_public.csv')
# question_dict = pd.Series(schema_df.iloc[:,1].values, index = schema_df.iloc[:,0]).to_dict()
raw_survey_df = raw_survey_df.rename(columns={'LanguageHaveWorkedWith': 'Language'})

schema_raw = schema_df.question
# print(schema_raw['Age'])





## Some testing I did with trying to manage and move around data to work in an easier manner. Trial and error
# schema_filter = schema_df[schema_df['qname'].isin(raw_survey_df.columns)]

# merged_df = pd.DataFrame

# for _,row in schema_filter.iterrows():
#     column_name = row['qname']      # Column name in data file
#     extra_info = row['question']        # Extra info you want to retrieve

#     # Add the column from data_df and extra info as a new column
#     merged_df[column_name] = raw_survey_df[column_name]
#     merged_df[f"{column_name}_info"] = extra_info


## Now I can refer to the schema to get the full questions they were asked
#print(question_dict.get('Age'))

selected_columns = [
    # Demographics
    'Country',
    'Age',
    'EdLevel',
    # Programming experience
    'CodingActivities',
    'YearsCode',
    'YearsCodePro',
    'LearnCode',
    'LearnCodeOnline',
    'TechDoc',
    'WorkExp',
    'Language',
    # Employment
    'Employment',
    'DevType',
    'JobSat',
    'CompTotal',
    'Industry',
    'Frustration'
]


## Think about what questions may be useful!
# How does the experience in coding affect the level of pay?
# What's the most popular method of learning?
# How much does a master's affect your chance of developer
# These are all questions we can try to answer after trying to understand the basic data first through python
## Before these can be answered, we can use python to get a basic analysis of the data as shown below:


survey_df = raw_survey_df[selected_columns].copy()
schema = schema_raw[selected_columns]
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
# matplotlib inline

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'



# top_countries = survey_df.Country.value_counts().head(15)
# print(top_countries)

# plt.figure(figsize=(12,6))
# plt.xticks(rotation=75)
# plt.title(schema.Country)
# sns.barplot(x=top_countries.index, y=top_countries)
# plt.show()
# From the bar plot, we can see there is a big difference between the number 1 country (United States) and the demographic of people we are surveying




import folium 
countries_geojson = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
country_counts = survey_df.Country.value_counts()
country_counts_df = pd.DataFrame({ 'Country': country_counts.index, 'Count': country_counts.values})
country_counts_df
country_counts_df.at[0, 'Country'] = 'United States of America'
country_counts_df.at[12, 'Country'] = 'Russia'
m = folium.Map(location=[30, 0], zoom_start=2)

folium.Choropleth(
    geo_data=countries_geojson,
    data=country_counts_df,
    columns=["Country", "Count"],
    key_on="feature.properties.name",
    threshold_scale=[1, 30, 100, 300, 1_000, 3_000, 10_000, 13_000],
    fill_color="OrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Respondents",
).add_to(m)

## m.show_in_browser()
#  Here, we have now shown the differences with a visualization of the entire world for better understanding


## Another critical demographic is age, so we will look at that next:

import plotly.express as px
px.histogram(survey_df, x="Age", marginal="box", title='Age of Respondents')




## Now let's take a look at education level of those taking the survery in 2024
# sns.countplot(y=survey_df.EdLevel)
# plt.xticks(rotation=75);
# plt.title(schema['EdLevel'])
# plt.ylabel(None);




## Developer type analysis, this will let me see what everyone chose
# print(survey_df.DevType.value_counts())



# (survey_df.DevType.value_counts(normalize=True, ascending=True)*100).plot(kind='barh', color='g')
# plt.title(schema.DevType)
# plt.xlabel('Percentage')
# plt.show()

## From the graph shown above, we can see there an incredible gap the top 2 developer types. Full stack is almost double the second spot of back-end



## -- Time to ask more questions: What were the most used languages among those who took the survey?
# We will use a function to help convert a column containing a list of values like this into a dataframe we can work with
def split_multicolumn(col_series):
    result_df = col_series.to_frame()
    options = []
    # Iterate over the column
    for idx, value  in col_series[col_series.notnull()].items():
        # Break each value into list of options
        for option in value.split(';'):
            # Add the option as a column to result
            if not option in result_df.columns:
                options.append(option)
                result_df[option] = False
            # Mark the value in the option column as True
            result_df.at[idx, option] = True
    return result_df[options]



# We will sort so that if the survey taker has chosen an option, the corresponing column value is True, otherwise false
languages_df = split_multicolumn(survey_df.Language)
language_totals = languages_df.sum().sort_values(ascending=False)
print(language_totals)

plt.figure(figsize=(12, 12))
sns.barplot(x=language_totals, y=language_totals.index)
plt.title("Languages used in the past year of 2024");
plt.xlabel('count');
plt.show()
#We can see the top 3 languages are Javascript, HTML/CSS, and Python!



## Let's see what the highest salaries are!
comp_total_values = survey_df['CompTotal'].sort_values(ascending=False)
print(comp_total_values)
# This might be an error, we see a top value of 1.0e+150 in Euro according to the excel. They may just make that much!






## We can continue to get a good understanding of the data set by doing analysis in python, but for better visualization of correlations, tableau will be more useful

