import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

request = requests.get('https://dataderden.cbs.nl/ODataApi/OData/47004NED/TypedDataSet')
table = json_normalize(json.loads(request.text)['value'])
table.to_csv('test.csv')
