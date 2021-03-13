import numpy as np
import pandas as pd

from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def gender():
    pd.options.display.max_columns = None

    people = pd.read_csv('people.csv', low_memory=False)
    name_gender = pd.read_csv('firstNameGender.csv', index_col=0)
    relationships = pd.read_csv('relationships.csv', low_memory=False)

    people["first_name"] = people["first_name"].str.replace("Dr.", "")
    people["first_name"] = people["first_name"].str.split("-").str[0]
    people["first_name"] = people["first_name"].str.split(" ").str[0]

    # Merge Gender, People and Relationsships
    people_gender = pd.merge(people, name_gender, on="first_name", how="left")
    people_gender.columns = ["id", "person_object_id", 'first_name', 'last_name', "birthplace", "affiliation_name",
                             "Gender"]

    result = pd.merge(people_gender, relationships, on="person_object_id", how="left")
    result = result.drop(
        columns=["person_object_id", "id_x", "id_y", "relationship_id", "start_at", "end_at", "is_past", "sequence",
                 "title", "created_at", "updated_at", 'first_name', 'last_name', "birthplace", "affiliation_name"])
    result.columns = ["gender", "object_id"]

    # Groupby Company ID
    result = result.groupby("object_id")["gender"].value_counts().unstack().fillna(0)
    # Calculation of female/male ratio
    result['sum'] = result['female'] + result['male']
    result['female'] = result['female'] / result['sum']
    result['male'] = result['male'] / result['sum']
    result = result.round({"female": 2, "male": 2})
    final_result = result.drop(columns=["sum"])

    return final_result



def prepare_training_data():
    companies_y = pd.read_csv('companies_y.csv', low_memory=False)
    companies_y = companies_y.drop('Unnamed: 0', 1)
    companies_y['funded_or_acquired'] = companies_y['funded_or_acquired'].astype(int)


    company_founding = pd.read_csv('company_founding.csv', low_memory=False)

    company_domain = pd.read_csv('company_domain.csv', low_memory=False)
    company_domain = company_domain.drop('Unnamed: 0', 1)
    company_domain = company_domain.drop('domain_name', 1)
    company_domain = company_domain.drop('domain', 1)
    company_domain = company_domain.drop('domain_ending', 1)
    company_domain.rename({'id': 'company_id'}, axis='columns', inplace=True)

    company_domain = company_domain.set_index("company_id")
    companies_y = companies_y.set_index("company_id")

    offices_cities_dummy = pd.read_csv('offices_cities_dummy.csv', low_memory=False)
    offices_cities_dummy.rename({'object_id': 'company_id'}, axis='columns', inplace=True)
    offices_cities_dummy = offices_cities_dummy.set_index("company_id")
    offices_cities_dummy.fillna(0)
    offices_cities_dummy.replace(np.nan, 0)
    offices_cities_dummy.replace('nan', 0)

    offices_cities_dummy = offices_cities_dummy.groupby('company_id').sum()



    offices_countries_dummy = pd.read_csv('offices_countries_dummy.csv', low_memory=False)
    offices_countries_dummy.rename({'object_id': 'company_id'}, axis='columns', inplace=True)
    offices_countries_dummy = offices_countries_dummy.set_index("company_id")
    offices_countries_dummy.fillna(0)
    offices_countries_dummy.replace(np.nan, 0)
    offices_countries_dummy.replace('nan', 0)

    offices_countries_dummy = offices_countries_dummy.groupby('company_id').sum()




    train = companies_y.join(company_domain, on="company_id", how='left')
    train = train.join(offices_cities_dummy, on="company_id", how='left')
    train = train.drop('Unnamed: 0', 1)
    #train = train.drop('city', 1)
    train = train.join(offices_countries_dummy, on="company_id", rsuffix = "_country", how='left')
    #train = train.drop('Unnamed: 0', 1)
    #train = train.drop('country_code', 1)
    train=train.fillna(0)
    #train.replace(np.nan, 0)

    gender_per_company = gender()

    train = train.join(gender_per_company, on="company_id", how='left')
    train = train.fillna(0.5)

    train = train.drop('male', 1)
    train = train.drop('Others', 1)
    train = train.drop('Others_country', 1)
    train = train.drop('Unnamed: 0', 1)


    return train

def model(data):
    #bulid the model
    #from: https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

    # split the dataset in training and testing data. This is a important step in
    # every machine learning project. But you will learn about this in detail in
    # your curriculum videos and exercises
    X = data.loc[:, data.columns != 'funded_or_acquired']
    y = data.loc[:, 'funded_or_acquired']

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)

    model = DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    # Evaluate predictions
    print("accuracy_score: "+ str(accuracy_score(Y_validation, predictions)))
    print("confusion_matrix:")
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


data = prepare_training_data()
model(data)






