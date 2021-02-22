import numpy as np
import pandas as pd
import requests
import json
from urllib.request import urlopen

#Daten einlesen
pd.options.display.max_columns = None
people = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/people.csv', low_memory=False)
relationships = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/relationships.csv', low_memory=False)

# Ethnicity:
# https://ethnicolr.readthedocs.io/ethnicolr.html#installation
# Gender API
# https://genderapi.io/api-documentation

people["first_name"] = people["first_name"].str.replace("Dr.", "")
people["first_name"] = people["first_name"].str.split("-").str[0]
people["first_name"] = people["first_name"].str.split(" ").str[0]


firstNames_unique = people.drop_duplicates(subset="first_name",keep='last')[["first_name","Gender"]]
firstNames_Gender = firstNames_unique.copy()
firstNames_Gender.reset_index(drop=True, inplace=True)

apiKey = "6027c00f0c5ad00e625f1f12"
# for i in range(len(firstNames_unique)):
for i in range(5):
  name = firstNames_unique.iloc[i]["first_name"]
  apiUrl = "https://genderapi.io/api/?name=" + name + "&key=" + apiKey
  result = urlopen(apiUrl).read().decode('utf-8')
  getGender = json.loads(result)
  firstNames_Gender.loc[[i], ["Gender"]] = getGender["gender"]

for i in range(len(people)):
     name = people.iloc[i]["first_name"]
     gender = firstNames_Gender[firstNames_Gender.first_name == name]["Gender"][0]
     people["Gender"][i] = gender

# Ethnicity
lastNames_unique = people.drop_duplicates(subset="last_name",keep='last')[["last_name"]]
lastNames_Ethnicity = lastNames_unique.copy()
lastNames_Ethnicity.reset_index(drop=True, inplace=True)
#function of ethnicolr
pred_census_ln(lastNames_Ethnicity, "last_name")
lastNames_Ethnicity.drop(columns=["api", "black", "hispanic","white"], inplace = True)

for i in range(len(people)):
    name = people.iloc[i]["last_name"]
    ethnicity =  lastNames_Ethnicity[lastNames_Ethnicity.last_name == name]["race"][0]
    people.loc[[i], ["Ethnicity"]] = ethnicity


