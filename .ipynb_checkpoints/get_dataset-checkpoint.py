
import pandas as pd
import requests
import json
from pandas.io.json import json_normalize


def get_datasets(request):
    tuples = []
    for line in json.loads(request.text)['value']:
        url = line['url']
        name = line['name']
        request = requests.get(url)
        table = json_normalize(json.loads(request.text)['value'])
        tuples.append((name,table))
        
    tables = {key: value for (key, value) in tuples}
    print(tables.keys())
    return tables

# Crime victims by personal characteristics 
url = "http://opendata.cbs.nl/ODataApi/OData/37957ENG"
request = requests.get(url)
tables = get_datasets(request)
df = tables['TypedDataSet']
df = df.loc[:, df.columns != 'ID']

#characteristics
df['KeyCharacteristics'] = [int(i) for i in df['PersonalCharacteristics']]

#dimension
df_characteristics = tables['PersonalCharacteristics']
df_characteristics['KeyCharacteristics'] = [int(i) for i in df_characteristics['Key']]
df_characteristics = df_characteristics[['Title','CategoryGroupID','KeyCharacteristics']]

#integration
df_victims_cha = pd.merge(df, df_characteristics, on='KeyCharacteristics', how='left')
df_victims_cha.index = df_victims_cha['Periods']
df_victims_cha.to_csv('data/crime_victims_personal_characteristics.csv', sep=',', encoding= 'utf-8')


# Deaths; murder and manslaughter, crime scene in The Netherlands
url = "https://opendata.cbs.nl/ODataApi/OData/81453ENG"
request = requests.get(url)
tables = get_datasets(request)
df = tables['TypedDataSet']
df = df.loc[:, df.columns != 'ID']

#integration
df_deaths = pd.merge(df, tables['Sex'], left_on='Sex', right_on='Key', how='left')
df_deaths = pd.merge(df, tables['Age'], left_on='Age', right_on='Key', how='left')
df_deaths.index = df_deaths['Periods']
df_deaths.to_csv('data/deaths_crime_scene.csv', sep=',', encoding= 'utf-8')



# Feelings of insecurity by background characteristics
url = "https://opendata.cbs.nl/ODataApi/OData/37775eng"
request = requests.get(url)
tables = get_datasets(request)
df = tables['TypedDataSet']
df = df.loc[:, df.columns != 'ID']

#characteristics
df['KeyCharacteristics'] = [int(i) for i in df['AllPersonalCharacteristics']]

#dimension
df_characteristics = tables['AllPersonalCharacteristics']
df_characteristics['KeyCharacteristics'] = [int(i) for i in df_characteristics['Key']]
df_characteristics = df_characteristics[['Title','CategoryGroupID','KeyCharacteristics']]

#integration
df_insecurity = pd.merge(df_insecurity, df_characteristics, on='KeyCharacteristics', how='left')
df_insecurity.index = df_insecurity['Periods']
df_insecurity.to_csv('data/feelings_insecurity_characteristics.csv', sep=',', encoding= 'utf-8')

