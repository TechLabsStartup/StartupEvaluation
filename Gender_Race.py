import numpy as np
import pandas as pd
import requests
import json
from urllib.request import urlopen


#Daten einlesen
pd.options.display.max_columns = None

people = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/people.csv', low_memory=False)
relationships = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/relationships.csv', low_memory=False)
people["Gender"] = ""

# TECHAPI
# https://ethnicolr.readthedocs.io/ethnicolr.html#installation
# name
# Alternative: https://gender-api.com/de/pricing
# BIRTHPLACE!

# Gender:
# Gender API
# https://genderapi.io/api-documentation

people["first_name"] = people["first_name"].str.replace("Dr.", "")
people["first_name"] = people["first_name"].str.split("-").str[0]
people["first_name"] = people["first_name"].str.split(" ").str[0]

#.sort_values(by="first_name")
firstNames_unique = people.drop_duplicates(subset="first_name",keep='last')[["first_name","Gender"]]
# firstNames_unique.to_csv('firstNames_unique.csv')

firstNames_Gender = firstNames_unique.copy()
# firstNames_Gender.to_csv('firstNames_Gender.csv')
firstNames_Gender.reset_index(drop=True, inplace=True)

apiKey = "6027c00f0c5ad00e625f1f12"

# for i in range(len(firstNames_unique)):
for i in range(5):
  name = firstNames_unique.iloc[i]["first_name"]
  apiUrl = "https://genderapi.io/api/?name=" + name + "&key=" + apiKey
  result = urlopen(apiUrl).read().decode('utf-8')
  getGender = json.loads(result)
  firstNames_Gender.loc[[i], ["Gender"]] = getGender["gender"]

print(firstNames_Gender)

# Ethnicity

lastNames_unique = people.drop_duplicates(subset="last_name",keep='last')[["last_name"]]
# lastNames_unique.to_csv('lastNames_unique.csv')
lastNames_Ethnicity = lastNames_unique.copy()
lastNames_Ethnicity.reset_index(drop=True, inplace=True)

pred_census_ln(lastNames_Ethnicity, "last_name")
lastNames_Ethnicity.drop(columns=["api", "black", "hispanic","white"], inplace = True)

print(lastNames_Ethnicity)