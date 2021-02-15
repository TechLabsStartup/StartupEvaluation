import numpy as np
import pandas as pd

#Importing the csv files and storing the data in dataframes.
objects = pd.read_csv('objects.csv', low_memory=False)
funding_rounds = pd.read_csv('funding_rounds.csv', low_memory=False)
acquisitions = pd.read_csv('acquisitions.csv', low_memory=False)

#Checking if companies had a funding round or were acquired. If yes, store 1 in a dummy variable.
def filter_y_data_and_join_on_companies():
    companies = objects[objects.entity_type == "Company"]

    funding_rounds_by_company = funding_rounds.groupby("object_id").count()
    funding_rounds_by_company["has_funding_from_funding_rounds_table"]=1
    funding_rounds_by_company_with_dummy = funding_rounds_by_company.filter(['object_id','has_funding_from_funding_rounds_table'])

    acquisitions_by_company = acquisitions.groupby("acquired_object_id").count()
    acquisitions_by_company["was_acquired"]=1
    acquisitions_by_company_with_dummy = acquisitions_by_company.filter(['acquired_object_id','was_acquired'])

    company_ids = companies.filter(['id', "funding_rounds"])
    company_ids.rename({'id': 'company_id'}, axis='columns', inplace=True)

    companies_y = company_ids.join(funding_rounds_by_company_with_dummy, on = "company_id")
    companies_y = companies_y.join(acquisitions_by_company_with_dummy, on = "company_id")
    companies_y.fillna(0, inplace = True)
    companies_y.loc[(companies_y.funding_rounds >= 1),'funding_rounds']=1
    companies_y.rename({'funding_rounds': 'has_funding_from_objects_table'}, axis='columns', inplace=True)
    companies_y["funded_or_acquired"]=companies_y["has_funding_from_objects_table"]+companies_y["has_funding_from_funding_rounds_table"]+companies_y["was_acquired"]
    companies_y.loc[(companies_y.funded_or_acquired >= 1),'funded_or_acquired']=1

    return companies_y.filter(['company_id', "funded_or_acquired"])

companies_y = filter_y_data_and_join_on_companies()

companies_y.to_csv('companies_y.csv')
