import pandas as pd
import numpy as np
from datetime import datetime


#Importing the csv files and storing the data in dataframes.
objects = pd.read_csv('objects.csv', low_memory=False)
companies = objects[objects.entity_type == "Company"]


def get_founding_date_info():
    #founding_date
    #founding_year
    #age_by_2013 Kaggle: The information is available up to December 2013 -> age = 01.12.2013 - founding_date

    company_founding = companies.filter(['id', "founded_at"])
    company_founding["founded_at"] = pd.to_datetime(company_founding["founded_at"])

    company_founding["founding_year"] = pd.DatetimeIndex(company_founding['founded_at']).year
    company_founding['founding_year'] = company_founding['founding_year'].fillna(0)
    company_founding['founding_year'] = company_founding['founding_year'].astype(int)

    date_format = "%Y-%m-%d"
    company_founding["age_by_2013"] = datetime.strptime('2013-12-01', date_format) - company_founding["founded_at"]
    company_founding['age_by_2013'] = company_founding['age_by_2013'].fillna(pd.Timedelta(seconds=0))

    return company_founding



def get_domain_info():
    #domain_name_length
    #domain_ending

    company_domain = companies.filter(['id', "domain"])
    company_domain["domain_name"] = company_domain.domain.str.split(".", expand=True)[0]

    company_domain["domain_name_length"] = company_domain["domain_name"].str.len()
    company_domain["domain_name_length"] = company_domain["domain_name_length"].fillna(0)
    company_domain["domain_name_length"] = company_domain["domain_name_length"].astype(int)

    company_domain["domain_ending"] = company_domain.domain.str.split(".", expand=True)[1]

    return company_domain

def domain_ending_dummy(company_domain):

    endings = company_domain.drop(columns=['domain_name', 'domain_name_length', 'domain'])

    endings['domain_ending'] = np.where(endings['domain_ending'].isin(['com', 'co', 'net', 'org', 'de', 'in', 'me', 'ca', 'tv', 'us', 'it', 'io', 'fr', 'ru', 'eu', 'nl', 'biz', 'es', 'se', 'ie']), endings['domain_ending'], 'Other')

    endings = pd.get_dummies(endings, columns=['domain_ending'])

    return endings




company_founding = get_founding_date_info()
company_domain = get_domain_info()
domain_ending_dummy = domain_ending_dummy(company_domain)


#company_founding.to_csv('company_founding.csv')
#company_domain.to_csv('company_domain.csv')
domain_ending_dummy.to_csv('domain_ending_dummy.csv')

