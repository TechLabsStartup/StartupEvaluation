import pandas as pd
import numpy as np

#Anzeige mehrerer Spalten
#pd.set_option("display.max_rows", 500, "display.max_columns", None)
pd.set_option("display.max_rows", None, "display.max_columns", None)

#Import
degrees = pd.read_csv('degrees.csv', low_memory=False)

#Übernahme aller relevanten Spalten
df = pd.DataFrame(degrees, columns = ['object_id', 'degree_type', 'subject', 'institution', 'graduated_at'])

#vorerst: nur Teildataset
dfshort = pd.DataFrame(degrees, columns = ['object_id', 'degree_type', 'subject'])

#Column Data Type aller Spalten: Object -->convert to String
#print(dfshort.dtypes)

#convert column types to string
dfshort = dfshort.convert_dtypes()
#print(dfshort.dtypes)

#Data Cleaning by Replacing
#Ersetze alle subjects die Business oder Finance enthalten mit Business -->| funktioniert noch nicht
#dfshort.loc[dfshort['subject'].str.contains('Business | Finance'), 'subject'] = 'Business'

#alle subjects in Kleinbuchstaben umwandeln
dfshort['subject'] = dfshort['subject'].str.lower()

#Kategorie Computer Science
# Anmerkung: viel Mix aus Electrical/Mathematics/Economics/Computer...-->Mischstudiengänge werden eindeutig kategorisiert
#abhängig vom Aufruf der FUnktion -->ggf. Computer Science & Mathematics
dfshort.loc[dfshort['subject'].str.contains('comput'), 'subject'] = 'Computer Science' #computer, computing etc.
dfshort.loc[dfshort['subject'].str.contains('software'), 'subject'] = 'Computer Science'
dfshort.loc[dfshort['subject'].str.contains('informat'), 'subject'] = 'Computer Science' #information, informatics
dfshort.loc[dfshort['subject'].str.contains('artificial'), 'subject'] = 'Computer Science'
dfshort.loc[dfshort['subject'].str.contains('eecs'), 'subject'] = 'Computer Science' #electrical engineering & computer sience
dfshort.loc[dfshort['subject'].str.contains('machine l'), 'subject'] = 'Computer Science' #machine learning
dfshort.loc[dfshort['subject'].str.contains('game'), 'subject'] = 'Computer Science' #gaming, game design etc.
dfshort.loc[dfshort['subject'].str.contains('programming'), 'subject'] = 'Computer Science'
dfshort.loc[dfshort['subject'].str.contains('data'), 'subject'] = 'Computer Science'
#später/zum Schluss: it mit Computer science ersetzen, zuvor zu viele Überschneidungen
#ebenso: cs = computer science zum Schluss

#Kategorie Engineering
dfshort.loc[dfshort['subject'].str.contains('elec'), 'subject'] = 'Engineering'
dfshort.loc[dfshort['subject'].str.contains('mechan'), 'subject'] = 'Engineering'
dfshort.loc[dfshort['subject'].str.contains('engine'), 'subject'] = 'Engineering'
dfshort.loc[dfshort['subject'].str.contains('telecommunication'), 'subject'] = 'Engineering' #telecommunciation engineering
dfshort.loc[dfshort['subject'].str.contains('robot'), 'subject'] = 'Engineering'
dfshort.loc[dfshort['subject'].str.contains('material'), 'subject'] = 'Engineering'
dfshort.loc[dfshort['subject'].str.contains('aero'), 'subject'] = 'Engineering'#aeronautics
#später: ee = electrical engineering

#Kategorie Mathematics
dfshort.loc[dfshort['subject'].str.contains('math'), 'subject'] = 'Mathematics'
dfshort.loc[dfshort['subject'].str.contains('operations research'), 'subject'] = 'Mathematics'
dfshort.loc[dfshort['subject'].str.contains('statistics'), 'subject'] = 'Mathematics'

#Kategorie Natural Sciences (Physics, Chemistry, Biology)
dfshort.loc[dfshort['subject'].str.contains('physic'), 'subject'] = 'Natural Sciences'
dfshort.loc[dfshort['subject'].str.contains('chemi'), 'subject'] = 'Natural Sciences'
dfshort.loc[dfshort['subject'].str.contains('bio'), 'subject'] = 'Natural Sciences'
dfshort.loc[dfshort['subject'].str.contains('neuroscience'), 'subject'] = 'Natural Sciences'
dfshort.loc[dfshort['subject'].str.contains('geneti'), 'subject'] = 'Natural Sciences' #genetics etc.
dfshort.loc[dfshort['subject'].str.contains('zoo'), 'subject'] = 'Natural Sciences' #zoology etc.
dfshort.loc[dfshort['subject'].str.contains('physio'), 'subject'] = 'Natural Sciences' #physiology etc.
dfshort.loc[dfshort['subject'].str.contains('immuno'), 'subject'] = 'Natural Sciences' #immunology.

#Kategorie Social Sciences (Anthropology, Economics, Geography, Political Science, Psychology, Sociology)
dfshort.loc[dfshort['subject'].str.contains('econom'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('poli'), 'subject'] = 'Social Sciences' #politics, political etc.
dfshort.loc[dfshort['subject'].str.contains('psyc'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('international relations'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('sociology'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('govern'), 'subject'] = 'Social Sciences' #government
dfshort.loc[dfshort['subject'].str.contains('social'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('geograph'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('anthrop'), 'subject'] = 'Social Sciences' #anthropology
dfshort.loc[dfshort['subject'].str.contains('europ'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('diplomac'), 'subject'] = 'Social Sciences'
dfshort.loc[dfshort['subject'].str.contains('public'), 'subject'] = 'Social Sciences'

#Kategorie Humanities (Visual Arts, History, Languages and Literatures, Law, Philosophy, Theology)
dfshort.loc[dfshort['subject'].str.contains('law'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('histo'), 'subject'] = 'Humanities' #historical, history
dfshort.loc[dfshort['subject'].str.contains('engl'), 'subject'] = 'Humanities' #english / language
dfshort.loc[dfshort['subject'].str.contains('philo'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('commun'), 'subject'] = 'Humanities' #communication
dfshort.loc[dfshort['subject'].str.contains('journ'), 'subject'] = 'Humanities' #journalism
dfshort.loc[dfshort['subject'].str.contains('architect'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('arts'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('j.d.'), 'subject'] = 'Humanities' #doctor of law
dfshort.loc[dfshort['subject'].str.contains('jd'), 'subject'] = 'Humanities' #doctor of law
dfshort.loc[dfshort['subject'].str.contains('juris'), 'subject'] = 'Humanities' #juris doctor
dfshort.loc[dfshort['subject'].str.contains('music'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('american'), 'subject'] = 'Humanities' #american studies/literature/culture
dfshort.loc[dfshort['subject'].str.contains('literature'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('photo'), 'subject'] = 'Humanities' #photography
dfshort.loc[dfshort['subject'].str.contains('spanish'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('french'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('film'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('media'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('theology'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('fashion'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('lega'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('japan'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('russia'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('languag'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('german'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('paint'), 'subject'] = 'Humanities' #painting etc.
dfshort.loc[dfshort['subject'].str.contains('linguis'), 'subject'] = 'Humanities' #linguistics etc.
dfshort.loc[dfshort['subject'].str.contains('asia'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('relig'), 'subject'] = 'Humanities' #religion, religous etc.
dfshort.loc[dfshort['subject'].str.contains('actin'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('writ'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('theat'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('cinema'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('chinese'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('china'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('education'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('graphic'), 'subject'] = 'Humanities'
dfshort.loc[dfshort['subject'].str.contains('design'), 'subject'] = 'Humanities'

#Kategorie Medical and Health
dfshort.loc[dfshort['subject'].str.contains('medic'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('pharma'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('nursing'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('health'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('nutrition'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('epidemi'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('clinic'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('neurolo'), 'subject'] = 'Medical and Health'
dfshort.loc[dfshort['subject'].str.contains('pathology'), 'subject'] = 'Medical and Health'

#Kategorie Business
dfshort.loc[dfshort['subject'].str.contains('business'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('financ'), 'subject'] = 'Business' #Finance & Financial
dfshort.loc[dfshort['subject'].str.contains('manag'), 'subject'] = 'Business' #management,managerial,managing
dfshort.loc[dfshort['subject'].str.contains('marketing'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('account'), 'subject'] = 'Business' #Accounting & Accountancy
dfshort.loc[dfshort['subject'].str.contains('mba'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('m.b.a'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('entrepr'), 'subject'] = 'Business' #entrepreneurial, entrepreneur
dfshort.loc[dfshort['subject'].str.contains('lead'), 'subject'] = 'Business' #leadership etc.
dfshort.loc[dfshort['subject'].str.contains('administration'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('strateg'), 'subject'] = 'Business' #strategy & strategic
dfshort.loc[dfshort['subject'].str.contains('venture'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('commerc'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('advertis'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('trad'), 'subject'] = 'Business' #trade, trading
dfshort.loc[dfshort['subject'].str.contains('tax'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('human resour'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('real estate'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('executive'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('sales'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('innovation'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('bank'), 'subject'] = 'Business'
dfshort.loc[dfshort['subject'].str.contains('supply'), 'subject'] = 'Business'

#Generell: überprüfe mögliche Überschneidungen (Stichwörter müssen eindeutig zu Kategorie passen)

#Kategorie Unknown: ??? ergibt Fehlermeldung
#dfshort.loc[dfshort['subject'].str.contains('????????'), 'subject'] = 'Unknown'

#erst ganz zum Schluss oder alles in Others/Unknown zum Schluss?
#Wie wichtig ist die Unterscheidung Unknown (empty) und Others?
#dfshort.loc[dfshort['subject'].str.contains('degree'), 'subject'] = 'Unknown'
#dfshort.loc[dfshort['subject'].str.contains('phd'), 'subject'] = 'Unknown'
#dfshort.loc[dfshort['subject'].str.contains('graduate'), 'subject'] = 'Unknown'
#dfshort.loc[dfshort['subject'].str.contains('honors'), 'subject'] = 'Unknown'

#Ausgabe Gesamtdatei
#print(dfshort)

#Ausgabe Zusammenfassung
print(dfshort.describe(include="all"))

#transform to csv again (leider nur ersten 16.000 nicht alle 100.000)
#dfshort.to_csv('/Users/Basti/Desktop/Test4.csv')



