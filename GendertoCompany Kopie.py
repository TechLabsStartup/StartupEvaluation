import numpy as np
import pandas as pd
pd.options.display.max_columns = None

people = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/people.csv', low_memory=False)
name_gender = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/firstNameGender.csv',index_col=0)
relationships = pd.read_csv('/Users/schultemarius/Desktop/TUM/Techlabs/archive/relationships.csv', low_memory=False)

people["first_name"] = people["first_name"].str.replace("Dr.", "")
people["first_name"] = people["first_name"].str.split("-").str[0]
people["first_name"] = people["first_name"].str.split(" ").str[0]

#Merge Gender, People and Relationsships
people_gender = pd.merge (people,name_gender, on ="first_name",how= "left")
people_gender.columns = ["id","person_object_id",'first_name', 'last_name',"birthplace","affiliation_name","Gender"]

result  = pd.merge (people_gender,relationships, on ="person_object_id",how= "left")
result = result.drop(columns=["person_object_id","id_x","id_y","relationship_id","start_at","end_at","is_past","sequence","title","created_at","updated_at",'first_name', 'last_name',"birthplace","affiliation_name"])
result.columns = ["gender","object_id"]

# Groupby Company ID
result = result.groupby("object_id")["gender"].value_counts().unstack().fillna(0)
# Calculation of female/male ratio
result['sum'] = result['female'] + result['male']
result['female'] = result['female'] /result['sum']
result['male'] = result['male'] /result['sum']
result = result.round({"female": 2, "male": 2})
final_result = result.drop(columns=["sum"])



