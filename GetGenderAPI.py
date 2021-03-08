import numpy as np
import pandas as pd
import requests
import json
from urllib.request import urlopen

#Daten einlesen
pd.options.display.max_columns = None
people = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/people.csv', low_memory=False)
relationships = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/relationships.csv', low_memory=False)

people["first_name"] = people["first_name"].str.replace("Dr.", "")
people["first_name"] = people["first_name"].str.split("-").str[0]
people["first_name"] = people["first_name"].str.split(" ").str[0]

firstNames_unique = people.drop_duplicates(subset="first_name",keep='last')[["first_name"]]
firstNames_Gender = firstNames_unique.copy()
firstNames_Gender["Gender"] = np.nan
firstNames_Gender.reset_index(drop=True, inplace=True)

apiKey = "603d224c396e4774dc3e9ab2"

for i in range(len(firstNames_unique)):
  valid_utf8 = True
  name = firstNames_unique.iloc[i]["first_name"]
  try:
      apiUrl = "https://genderapi.io/api/?name=" + name + "&key=" + apiKey
      result = urlopen(apiUrl).read().decode('utf-8')
  except:
      valid_utf8 = False
      firstNames_Gender.loc[[i], ["Gender"]] = "null"
      print(name)
      continue
  getGender = json.loads(result)
  firstNames_Gender.loc[[i], ["Gender"]] = getGender["gender"]
  firstNames_Gender.to_csv(r"/Users/schultemarius/Desktop/firstNameGender.csv", index=False)








