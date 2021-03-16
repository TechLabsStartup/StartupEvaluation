
import numpy as np
import pandas as pd

people = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/people.csv', low_memory=False)
relationships = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/relationships.csv', low_memory=False)
name_race = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/lastNameRace.csv',index_col=0)

people["last_name"] = people["last_name"].astype(str)

people["last_name"] = people["last_name"].apply(lambda x: max(x.split("."), key=len))
people["last_name"] = people["last_name"].apply(lambda x: max(x.split(" "), key=len))
people["last_name"] = people["last_name"].apply(lambda x: max(x.split("-"), key=len))

#Merge Gender, People and Relationsships

people_race = pd.merge (people,name_race, on ="last_name",how= "left")

people_race.columns = ["id","person_object_id",'first_name', 'last_name',"birthplace","affiliation_name","Gender"]

result  = pd.merge (people_race,relationships, on ="person_object_id",how= "left")
result = result.drop(columns=["person_object_id","id_x","id_y","relationship_id","start_at","end_at","is_past","sequence","title","created_at","updated_at",'first_name', 'last_name',"birthplace","affiliation_name"])
result.columns = ["race","object_id"]



# Groupby Company ID
result = result.groupby("object_id")["race"].value_counts().unstack().fillna(0)
# Calculation of race - ratio
result['sum'] = result['api'] + result['black'] + result['hispanic'] + result['white']
result['asian'] = result['api'] /result['sum']
result['black'] = result['black'] /result['sum']
result['hispanic'] = result["hispanic"] /result['sum']
result['white'] = result["white"] /result['sum']

result = result.round({"white": 2, "asian": 2,"black": 2, "hispanic": 2})


final_result = result.drop(columns=["sum","api"])
print(final_result)