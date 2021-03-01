import pandas as pd
import numpy as np

#Import
degrees = pd.read_csv('degrees.csv', low_memory=False)
people = pd.read_csv('people.csv', low_memory=False)
relationships = pd.read_csv('relationships.csv', low_memory=False )
objects = pd.read_csv('objects.csv', low_memory=False )

#Übernahme aller relevanten Spalten
#df = pd.DataFrame(degrees, columns = ['object_id', 'degree_type', 'subject', 'institution', 'graduated_at'])

#vorerst: nur Teildataset
dfshort = pd.DataFrame(degrees, columns = ['object_id', 'degree_type', 'subject'])
dfpeople = pd.DataFrame(people, columns = ['object_id', 'first_name', 'last_name'])
#dfrelationships = pd.DataFrame(relationships, columns = ['person_object_id', 'relationship_object_id'])
#dfobjects = pd.DataFrame(objects, columns = ['entity_id', 'name'])

#Merge/Join tables -->error: int zu Object
#dfshort.object_id.astype(str)
#dfpeople.object_id.astype(str)
#dfshort = dfshort.join(dfpeople, on = 'object_id')
#print(dfshort.dtypes)
#print(dfpeople.dtypes)

#Part 1: subjects

#Spalte pro Kategorie hinzufügen mit Anfangswert 0 (für Dummy Variablen):
dfshort['Computer Science'] = 0
dfshort['Engineering'] = 0
dfshort['Mathematics'] = 0
dfshort['Natural Sciences'] = 0
dfshort['Social Sciences'] = 0
dfshort['Humanities'] = 0
dfshort['Medical and Health'] = 0
dfshort['Business'] = 0
dfshort['Others'] = 0

#Column Data Type aller Spalten: Object -->convert to String
#print(dfshort.dtypes)

#convert column types to string
dfshort = dfshort.convert_dtypes()
#print(dfshort.dtypes)

def dummy(ausgangstabelle, schlagwort, kategorietabelle):
    dfshort.loc[dfshort[ausgangstabelle].str.contains(schlagwort), kategorietabelle] = 1

#Data Cleaning by Replacing
#dfshort.loc[dfshort['subject'].str.contains('Business | Finance'), 'subject'] = 'Business'

#alle subjects in Kleinbuchstaben umwandeln
dfshort['subject'] = dfshort['subject'].str.lower()

#Kategorie Computer Science
compScienceList = ['comput', 'software', 'informat', 'artifical', 'artificial', 'eecs', 'machine l', 'game', 'programming', 'data']
for i in compScienceList:
    dummy('subject', i, 'Computer Science')

# ebenso: cs = computer science -->ohne contains, sondern Gleichheit
dfshort.loc[(dfshort['subject'] == 'it'), 'Computer Science'] = 1
dfshort.loc[(dfshort['subject'] == 'cs'), 'Computer Science'] = 1

#Kategorie Engineering
engineeringList = ['elec', 'mechan', 'engine', 'telecommunication', 'robot', 'material', 'aero']
for i in engineeringList:
    dummy('subject', i, 'Engineering')
#später: ee = electrical engineering -->ohne contains, sondern Gleichheit
dfshort.loc[(dfshort['subject'] == 'ee'), 'Engineering'] = 1

#Kategorie Mathematics
mathematicList = ['math', 'operations research', 'statistics']
for i in mathematicList:
    dummy('subject', i, 'Mathematics')

#Kategorie Natural Sciences (Physics, Chemistry, Biology)
naturalScienceList = ['physic', 'chemi', 'bio', 'neuroscience', 'geneti', 'zoo', 'physio', 'immuno']
for i in naturalScienceList:
    dummy('subject', i, 'Natural Sciences')

#Kategorie Social Sciences (Anthropology, Economics, Geography, Political Science, Psychology, Sociology)
socialScienceList = ['econom','poli','psyc', 'international relations', 'sociology', 'govern', 'social',
                     'geograph', 'anthrop', 'europ', 'diplomac', 'public', 'geology']
for i in socialScienceList:
    dummy('subject', i, 'Social Sciences')

#Kategorie Humanities (Visual Arts, History, Languages and Literatures, Law, Philosophy, Theology)
humanitiesList = ['law','histo','engl','philo','commun','journ','architect','art','j.d.','jd','juris',
                  'music','american','literature','photo','spanish','french','film','media','theology',
                  'fashion','lega','japan','russia','languag','german','paint','linguis','asia','relig',
                  'actin','writ','theat','cinema','chinese','china','education','graphic','design']
for i in humanitiesList:
    dummy('subject', i, 'Humanities')

# falls JD in Spalte degree_type ebenso Humanities Kategorie
dummy('degree_type', 'JD', 'Humanities')

#Kategorie Medical and Health
medicalHealthList = ['medic','pharma', 'nursing', 'health','nutrition','epidemi','clinic','neurolo','pathology' ]
for i in medicalHealthList:
    dummy('subject', i, 'Medical and Health')

#Kategorie Business
businessList = ['business','financ','manag','marketing','account','mba','m.b.a','entrepr','lead','administration',
                'strateg','venture','commerc','advertis','trad','tax','human resour','real estate','executive',
                'sales','innovation','bank','supply']
for i in businessList:
    dummy('subject', i, 'Business')

#falls MBA Titel in Spalte degree_type hat ebenso Business Kategorie
dummy('degree_type', 'MBA', 'Business')

#Kategorie Others (wenn alle anderen Kategorien nicht zutreffen, also 0 sind
dfshort.loc[(dfshort['Computer Science'] == 0) & (dfshort['Engineering'] == 0) & (dfshort['Mathematics'] == 0)
& (dfshort['Natural Sciences'] == 0) & (dfshort['Social Sciences'] == 0) & (dfshort['Humanities'] == 0)
& (dfshort['Medical and Health'] == 0) & (dfshort['Business'] == 0), 'Others'] = 1

#Part 2: still to do: degree titel + university


#Ausgabe Zusammenfassung
#print(dfshort.describe(include="all"))

#transform to csv again (leider nur ersten 16.000 nicht alle 100.000)
#dfshort.to_csv('/Users/Basti/Desktop/Test6.csv')





