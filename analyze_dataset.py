import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

model_data = pd.read_csv('data.csv', low_memory=False)
model_data = model_data.set_index('company_id')
y_mean = model_data["funded_or_acquired"].mean()
plt.rcParams["figure.figsize"] = (15, 10)


def analyze(column_name, dataset):
    analysis = dataset.groupby([column_name])['funded_or_acquired'].mean()
    analysis.sort_values(inplace=True, ascending=False)
    ax = analysis.plot.bar(color='tab:blue')
    ax.set(ylabel="mean of funded/acquired")
    plt.axhline(y=y_mean, color='k', linestyle='--')
    ax.set_xlabel(column_name, fontsize=20)
    ax.set_ylabel("mean of funded/acquired", fontsize=20)
    ax.tick_params(labelsize=15)
    for item in ax.get_xticklabels():
        if column_name == "cities":
            item.set_rotation(0)
    filename = column_name + "_analysis.png"
    plt.savefig(filename)
    plt.show()
    return analysis

def create_bins_and_analyze(column_name, dataset, bin_step):
    dataset['bin'] = dataset[column_name].apply(lambda x: bin_step * np.floor(x / bin_step))
    analysis = dataset.groupby('bin')['funded_or_acquired'].mean()
    analysis = analysis.to_frame()
    analysis[column_name] = analysis.index
    x = analysis[column_name].round(2)
    x.reset_index(inplace=True, drop=True)
    y = analysis['funded_or_acquired']
    y.reset_index(inplace=True, drop=True)
    ax = sns.barplot(x=x, y=y, color='tab:blue')
    ax.set(ylabel="mean of funded/acquired")
    plt.axhline(y=y_mean, color='k', linestyle='--')
    ax.set_xlabel(column_name, fontsize=20)
    ax.set_ylabel("mean of funded/acquired", fontsize=20)
    ax.tick_params(labelsize=15)
    if column_name == "black":
        ax.set_xlabel("percentage of black founders", fontsize=20)
    filename = column_name + "_analysis.png"
    plt.savefig(filename)
    plt.show()
    return analysis

def undummy(columns, dataset, name):
    y = dataset['funded_or_acquired']
    data = dataset[columns]
    data = data.idxmax(axis=1)
    y = y.to_frame()
    data = data.to_frame()
    all = y.join(data, on="company_id", how='left')
    all.rename({0: name}, axis='columns', inplace=True)
    all[name] = all[name].str.replace('domain_ending_', '')
    return all

#domain_name_length_analysis = analyze('domain_name_length', model_data)
domain_name_length_analysis_binned = create_bins_and_analyze('domain_name_length', model_data, 5)

female_male_ratio_analysis = create_bins_and_analyze('female', model_data, 0.1)

black_percentage_analysis = create_bins_and_analyze('black', model_data, 0.1)
hispanic_percentage_analysis = create_bins_and_analyze('hispanic', model_data, 0.1)
white_percentage_analysis = create_bins_and_analyze('white', model_data, 0.1)
asian_percentage_analysis = create_bins_and_analyze('asian', model_data, 0.1)

countries_undummied = undummy(['USA','GBR','IND','CAN','DEU','FRA','AUS','ESP','ISR','CHN','IRL','NLD'], model_data, 'countries')
countries_undummied_analysis = analyze('countries', countries_undummied)

cities_undummied = undummy(['New York','San Francisco','London','Chicago','Los Angeles','Paris','Seattle','Austin','Boston','Atlanta','Bangalore','Berlin','Tokyo','New Delhi','Amsterdam','Beijing','Moscow','Shanghai','Tel Aviv','Sao Paulo'], model_data, 'cities')
cities_undummied_analysis = analyze('cities', cities_undummied)

cities_USA_undummied = undummy(['New York','San Francisco','Chicago','Los Angeles','Seattle','Austin','Boston','Atlanta'], model_data, 'cities')
cities_USA_undummied_analysis = analyze('cities', cities_USA_undummied)

cities_USA_reduced_undummied = undummy(['New York','San Francisco','Chicago','Los Angeles'], model_data, 'cities')
cities_USA_reduced_undummied_analysis = analyze('cities', cities_USA_reduced_undummied)

domain_ending_undummied = undummy(['domain_ending_Other','domain_ending_biz','domain_ending_ca','domain_ending_co','domain_ending_com','domain_ending_de','domain_ending_es','domain_ending_eu','domain_ending_fr','domain_ending_ie','domain_ending_in','domain_ending_io','domain_ending_it','domain_ending_me','domain_ending_net','domain_ending_nl','domain_ending_org','domain_ending_ru','domain_ending_se','domain_ending_tv','domain_ending_us'], model_data, 'domain_ending')
domain_ending_undummied_analysis = analyze('domain_ending', domain_ending_undummied)

