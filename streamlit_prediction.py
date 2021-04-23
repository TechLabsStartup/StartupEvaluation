
import streamlit as st
import pickle
import pandas as pd
import numpy as np

#pickle_in = open('decision_tree_model.pkl', 'rb')
pickle_in = open('decision_tree_regressor_model.pkl', 'rb')
#pickle_in = open('/Users/schultemarius/Documents/GitHub/StartupEvaluation/decision_tree_regressor_model.pkl', 'rb')
#pickle_in = open('/Users/schultemarius/Documents/GitHub/StartupEvaluation/decision_tree_model.pkl', 'rb')
classifier = pickle.load(pickle_in)

st.title('Will your Startup be successful?')
st.markdown("***")
firstname1 = st.text_input("First Name of the founder 1:")
lastname1 = st.text_input("Last Name of the founder 1:")
firstname2 = st.text_input("First Name of the founder 2:")
lastname2 = st.text_input("Last Name of the founder 2:")
firstname3 = st.text_input("First Name of the founder 3:")
lastname3 = st.text_input("Last Name of the founder 3:")
university = st.text_input("University where the CEO studied") ## Drop Down
major = st.text_input("University Major of the CEO")
city = st.selectbox("City where the Startup operates", ("Munich","Amsterdam","Atlanta","Austin","Bangalore","Beijing","Berlin","Boston","Chicago","London","Los Angeles","Moscow","New Delhi","New York","Paris","San Francisco","Sao Paulo","Seattle","Shanghai","Tel Aviv","Tokyo","Other"))
country = st.selectbox("Country where the Startup operate", ("DEU","AUS","CAN","CHN","ESP","FRA","GBR","IND","IRL","ISR","NLD","USA","Other" ))
domain= st.text_input("Website") ## Drop Down

#Error Message fehlt

submit = st.button('Predict')

if submit:

    # Modify Data
    # People
    # get Gender
    name_gender = pd.read_csv('https://raw.githubusercontent.com/TechLabsStartup/StartupEvaluation/main/firstNameGender.csv', index_col=0)

    people = {'first_name': [firstname1, firstname2, firstname3]}
    people = pd.DataFrame(people)
    people["first_name"] = people["first_name"].astype(str)
    people["first_name"] = people["first_name"].str.replace("Dr.", "")
    people["first_name"] = people["first_name"].str.split("-").str[0]
    people["first_name"] = people["first_name"].str.split(" ").str[0]
    people_gender = pd.merge(people, name_gender, on="first_name", how="left")
    female = people_gender.Gender.str.count("female").sum()
    female = round((female / 3), 2)

    # People
    # get Race
    name_race = pd.read_csv('https://raw.githubusercontent.com/TechLabsStartup/StartupEvaluation/main/lastNameRace.csv', index_col=0)

    people = {'last_name': [lastname1, lastname2, lastname3]}
    people = pd.DataFrame(people)
    people["last_name"] = people["last_name"].astype(str)
    people["last_name"] = people["last_name"].apply(lambda x: max(x.split("."), key=len))
    people["last_name"] = people["last_name"].apply(lambda x: max(x.split(" "), key=len))
    people["last_name"] = people["last_name"].apply(lambda x: max(x.split("-"), key=len))

    people_race = pd.merge(people, name_race, on="last_name", how="left")
    asian = round((people_race.race.str.count("api").sum() / 3), 2)
    black = round((people_race.race.str.count("black").sum() / 3), 2)
    hispanic = round((people_race.race.str.count("hispanic").sum() / 3), 2)
    white = round((people_race.race.str.count("white").sum() / 3), 2)

    column_names = ["domain_name_length","New York","San Francisco","London","Chicago","Los Angeles","Paris","Seattle","Austin","Boston","Atlanta","Bangalore","Berlin","Tokyo","New Delhi","Amsterdam","Beijing","Moscow","Shanghai","Tel Aviv","Sao Paulo","USA","GBR","IND","CAN","DEU","FRA","AUS","ESP","ISR","CHN","IRL","NLD","female","black","hispanic","white","asian","domain_ending_Other","domain_ending_biz","domain_ending_ca","domain_ending_co","domain_ending_com","domain_ending_de","domain_ending_es","domain_ending_eu","domain_ending_fr","domain_ending_ie","domain_ending_in","domain_ending_io","domain_ending_it","domain_ending_me","domain_ending_net","domain_ending_nl","domain_ending_org","domain_ending_ru","domain_ending_se","domain_ending_tv","domain_ending_us"]
    result = pd.DataFrame(columns = column_names)
    result.loc[1] = 0

    # domain
    # Length
    domain_ending = domain.split(".")[-1]
    company_domain_length = len(domain)

    #Was ist die Domain length? auch das www. oder nur facebook?

    list_of_string =['com', 'co', 'net', 'org', 'de', 'in', 'me', 'ca', 'tv', 'us', 'it', 'io', 'fr', 'ru', 'eu', 'nl', 'biz', 'es',
         'se', 'ie']
    if domain_ending not in list_of_string:
        domain_ending = "Other"

    domain_result = "domain_ending_"
    domain_result += domain_ending

##########################################

    if city not in ("Munich", "Other"):
        city = str(city)
        result.loc[1, city] = 1

    if country != "Other":
        country = str(country)
        result.loc[1, country] = 1

    result.loc[1, 'female'] = female
    result.loc[1, 'white'] = white
    result.loc[1, 'black'] = black
    result.loc[1, 'hispanic'] = hispanic
    result.loc[1, 'asian'] = asian
   #result.loc[1, city] = 1
   #result.loc[1, country]= 1
    result.loc[1, domain_result] = 1
    result.loc[1, "domain_name_length"] = company_domain_length

    check = False
    list_of_str = [firstname1, domain, university, major]
    for elem in list_of_str:
        # Check if string is empty or contain only spaces
        if elem == "":
            check = True
            break;

    if check:
        st.markdown("***")
        st.error("Please input data")
    else:
        prediction = classifier.predict(result)

        if prediction >= 0.5:
            if prediction == 1.0:
               prediction -= 0.01
            st.markdown("***")
            st.success('Congratulations! Your Startup will be successful')
            prediction = prediction.item(0)
            st.success("The probability of success is: "+'{:.2%}'.format(prediction))
            #st.write("![Alt Text](https://media.giphy.com/media/dAcn0Q09BfHOP8eGp7/source.mp4)", width=700)
            st.image("photoWinner.jpg")
            #st.image("/Users/schultemarius/Documents/GitHub/StartupEvaluation/photoWinner.jpg")
        else:
            st.markdown("***")
            st.error(" We are really sorry to say you that your Startup will not be successful.")
            # st.write("![Alt Text](https://media.giphy.com/media/kZj0PZtAJeiYYvnM3f/source.mp4)", width=700)
            st.image("photoLoser.jpg")
            #st.image("/Users/schultemarius/Documents/GitHub/StartupEvaluation/photoLoser.jpg")


# RUN in Terminal:streamlit run /Users/schultemarius/Documents/GitHub/StartupEvaluation/streamlit_prediction.py
# streamlit run streamlit_prediction.py
#




