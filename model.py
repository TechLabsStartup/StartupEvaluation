import numpy as np
import pandas as pd
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle


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

def prepare_data():
    companies_y = pd.read_csv('companies_y.csv', low_memory=False)
    companies_y = companies_y.drop('Unnamed: 0', 1)
    companies_y['funded_or_acquired'] = companies_y['funded_or_acquired'].astype(int)

    companies_races = pd.read_csv('racecompany.csv', low_memory=False)


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

    companies_races.rename({'object_id': 'company_id'}, axis='columns', inplace=True)
    companies_races = companies_races.set_index("company_id")
    train = train.join(companies_races, on="company_id", how='left')
    train=train.fillna(0)
    train = train.drop('Unnamed: 0', 1)


    domain_endings = pd.read_csv('domain_ending_dummy.csv', low_memory=False)
    domain_endings.rename({'id': 'company_id'}, axis='columns', inplace=True)
    domain_endings = domain_endings.set_index("company_id")
    train = train.join(domain_endings, on="company_id", how='left')
    train=train.fillna(0)
    train = train.drop('Unnamed: 0', 1)



    train = train.drop('male', 1)
    train = train.drop('Others', 1)
    train = train.drop('Others_country', 1)


    return train

def model_dt(data):
    #from: https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

    X = data.loc[:, data.columns != 'funded_or_acquired']
    y = data.loc[:, 'funded_or_acquired']

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.3, random_state=1, shuffle=True)

    model = DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    # Evaluate predictions
    print("accuracy_score: "+ str(accuracy_score(Y_validation, predictions)))
    print("confusion_matrix:")
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

    # Saving the Model
    pickle_out = open("decision_tree_model.pkl", "wb")
    pickle.dump(model, pickle_out)
    pickle_out.close()

    importance = model.feature_importances_
    # summarize feature importance
    #for i, v in enumerate(importance):
        #print('Feature: %0d, Score: %.5f' % (i, v))
    # plot feature importance
    pyplot.rcParams["figure.figsize"] = (15, 10)
    pyplot.bar([x for x in range(len(importance))], importance)
    pyplot.show()

    feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
    ax = feat_importances.nlargest(10).plot(kind='barh')
    ax.set(ylabel="feature (top 10)", xlabel="feature importance (decision tree classifier)")
    pyplot.savefig("decision_tree_feature_importances.png")
    pyplot.show()


    print("checking on training data:")
    model2 = DecisionTreeClassifier()
    model2.fit(X_train, Y_train)
    predictions2 = model2.predict(X_train)
    print("accuracy_score (training): "+ str(accuracy_score(Y_train, predictions2)))

    print("confusion matrix")
    print(confusion_matrix(Y_train, predictions2))

def model_gauss(data):
    X = data.loc[:, data.columns != 'funded_or_acquired']
    y = data.loc[:, 'funded_or_acquired']

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.3, random_state=1, shuffle=True)

    model = GaussianNB()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    # Evaluate predictions
    print("accuracy_score: "+ str(accuracy_score(Y_validation, predictions)))
    print("confusion_matrix:")
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


    print("checking on training data:")
    model2 = DecisionTreeClassifier()
    model2.fit(X_train, Y_train)
    predictions2 = model2.predict(X_train)
    print("accuracy_score (training): "+ str(accuracy_score(Y_train, predictions2)))

    print("confusion matrix")
    print(confusion_matrix(Y_train, predictions2))

def model_linear(data):
    X = data.loc[:, data.columns != 'funded_or_acquired']
    y = data.loc[:, 'funded_or_acquired']

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.3, random_state=1, shuffle=True)

    model = LogisticRegression(solver='liblinear', multi_class='ovr')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    # Evaluate predictions
    print("accuracy_score: "+ str(accuracy_score(Y_validation, predictions)))
    print("confusion_matrix:")
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


    print("checking on training data:")
    model2 = DecisionTreeClassifier()
    model2.fit(X_train, Y_train)
    predictions2 = model2.predict(X_train)
    print("accuracy_score (training): "+ str(accuracy_score(Y_train, predictions2)))

    print("confusion matrix")
    print(confusion_matrix(Y_train, predictions2))

    return model

def model_SVC(data):
    X = data.loc[:, data.columns != 'funded_or_acquired']
    y = data.loc[:, 'funded_or_acquired']

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.3, random_state=1, shuffle=True)

    model = SVC(gamma='auto')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    # Evaluate predictions
    print("accuracy_score: "+ str(accuracy_score(Y_validation, predictions)))
    print("confusion_matrix:")
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))



    print("checking on training data:")
    model2 = DecisionTreeClassifier()
    model2.fit(X_train, Y_train)
    predictions2 = model2.predict(X_train)
    print("accuracy_score (training): "+ str(accuracy_score(Y_train, predictions2)))

    print("confusion matrix")
    print(confusion_matrix(Y_train, predictions2))

def upsample_data(data):
    #from: https://elitedatascience.com/imbalanced-classes

    print("------")
    print("trying to balance the dataset using upsampling = duplicate funded startups until here are as many companies as non funded ones")

    print("summary of dataset: "+str(data.funded_or_acquired.value_counts()))

    # Separate majority and minority classes
    df_majority = data[data.funded_or_acquired == 0]
    df_minority = data[data.funded_or_acquired == 1]

    print("summary of majority: "+str(df_majority.funded_or_acquired.value_counts()))
    print("summary of minority: "+str(df_minority.funded_or_acquired.value_counts()))

    # Upsample minority class
    df_minority_upsampled = resample(df_minority,
                                     replace=True,  # sample with replacement
                                     n_samples=158045,  # to match majority class
                                     random_state=123)  # reproducible results

    # Combine majority class with upsampled minority class
    df_upsampled = pd.concat([df_majority, df_minority_upsampled])

    # Display new class counts
    print("after upsampling:")
    print(df_upsampled.funded_or_acquired.value_counts())

    return df_upsampled

def downsample_data(data):
    #from: https://elitedatascience.com/imbalanced-classes

    #print("------")
    #print("trying to balance the dataset using downsampling = delete un-funded startups until here are as many companies as non funded ones")

    #print("summary of dataset: "+str(data.funded_or_acquired.value_counts()))

    # Separate majority and minority classes
    df_majority = data[data.funded_or_acquired == 0]
    df_minority = data[data.funded_or_acquired == 1]

    #print("summary of majority: "+str(df_majority.funded_or_acquired.value_counts()))
    #print("summary of minority: "+str(df_minority.funded_or_acquired.value_counts()))

    # Upsample minority class
    df_majority_downsampled = resample(df_majority,
                                     replace=False,  # sample with replacement
                                     n_samples=38508,  # to match majority class
                                     random_state=123)  # reproducible results

    # Combine majority class with upsampled minority class
    df_downsampled = pd.concat([df_majority_downsampled, df_minority])

    # Display new class counts
    #print("after downsampling:")
    #print(df_downsampled.funded_or_acquired.value_counts())

    return df_downsampled


data = prepare_data()
data_downsampled = downsample_data(data)

print("---")
print("Decision Tree:")
model_dt(data_downsampled)
#print("---")
#print("GaussianNB:")
#model_gauss(data_downsampled)
#print("---")
#print("LogisticRegression:")
#m = model_linear(data_downsampled)
#print("---")
#print("SVC:")
#model_SVC(data_downsampled)



#data.to_csv('data.csv')








