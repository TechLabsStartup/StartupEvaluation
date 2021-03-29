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

#convert column types from object to string
dfshort = dfshort.convert_dtypes()
#print(dfshort.dtypes)

def dummy(ausgangstabelle, schlagwort, kategorietabelle):
    dfshort.loc[dfshort[ausgangstabelle].str.contains(schlagwort), kategorietabelle] = 1

#alle subjects in Kleinbuchstaben umwandeln
dfshort['subject'] = dfshort['subject'].str.lower()

#Kategorie Computer Science
compScienceList = ['comput', 'software', 'informat', 'artifical', 'artificial', 'eecs', 'machine l', 'game', 'programming', 'data']
for i in compScienceList:
    dummy('subject', i, 'Computer Science')

#ebenso: cs = computer science -->ohne contains, sondern Gleichheit
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

#Merge/Join tables -->error: int zu Object
#dfshort = dfshort.object_id.astype(str) #Ergebnis Abspeichern
#dfpeople = dfpeople.object_id.astype(str)
#dfshort = dfshort.join(dfpeople, on = 'object_id')
#print(dfshort.dtypes)
#print(dfpeople.dtypes)

#Part 2: still to do: degree titel + university
dfshort['degree_type'] = dfshort['degree_type'].str.lower()

#Spalte pro Kategorie hinzufügen mit Anfangswert 0 (für Dummy Variablen):
dfshort['Master'] = 0
dfshort['Bachelor'] = 0
dfshort['Phd'] = 0
dfshort['Unknown Degree'] = 0

#Kategorie Master:
masterList = ['mba', 'ms', 'master', 'jd', 'm.math', 'mps', 'mphil', 'mpa', 'meng', 'diplom',
              'post', 'j.d', 'mph', 'm.b.a', 'm.e', 'dipl']
for i in masterList:
    dummy('degree_type', i, 'Master')
dfshort.loc[(dfshort['degree_type'] == 'ma'), 'Master'] = 1
dfshort.loc[(dfshort['degree_type'] == 'mis'), 'Master'] = 1

#Kategorie Bachelor:
bachelorList = ['bcs', 'llb', 'bfa', 'bba', 'bache', 'bacs', 'bs', 'bcom','bsc', 'b.s', 'bachlelors',
                'b.business', 'b.engineering', 's.b', 'btech', 'beng', 'undergrad', 'scb', 'b.a.', 'bca','b.a' ]
for i in bachelorList:
    dummy('degree_type', i, 'Bachelor')
# später: ee = electrical engineering -->ohne contains, sondern Gleichheit
dfshort.loc[(dfshort['degree_type'] == 'be'), 'Bachelor'] = 1
dfshort.loc[(dfshort['degree_type'] == 'ba'), 'Bachelor'] = 1
dfshort.loc[(dfshort['degree_type'] == 'aa'), 'Bachelor'] = 1
dfshort.loc[(dfshort['degree_type'] == 'sb'), 'Bachelor'] = 1
dfshort.loc[(dfshort['degree_type'] == 'bs'), 'Bachelor'] = 1

#Kategorie Phd:
PhdList = ['phd', 'ph.d', 'dphil', 'md', 'doctor', 'dr']
for i in PhdList:
    dummy('degree_type', i, 'Phd')

#Idee: falls 1 bei Phd, 0 bei Master und Bachelor
#sowie falls 1 bei Master, dann 0 bei Bachelor

#Kategorie Unknown Degrees (wenn alle anderen Kategorien nicht zutreffen, also 0 sind:
dfshort.loc[(dfshort['Master'] == 0) & (dfshort['Bachelor'] == 0) & (dfshort['Phd'] == 0), 'Others'] = 1

#Ausgabe Zusammenfassung
#print(dfshort.describe(include="all"))

#transform to csv again
#dfshort.to_csv('/Users/Basti/Desktop/Testdegree2.csv')





