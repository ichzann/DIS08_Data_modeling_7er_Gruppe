import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('14-24.csv', sep=';')


Deutschland=df[df['Country']=='DE']
Deutschland=Deutschland.reset_index(drop=True)

df = df.drop(columns=['Metabolite','Site ID','Latitude','Longitude','Location','City.1','Country: City'])

Chemnitz=df[df['City'].str.startswith('Chemnitz')]
Chemnitz=Chemnitz.reset_index(drop=True)

Dortmund=df[df['City'].str.startswith('Dortmund')]
Dortmund=Dortmund.reset_index(drop=True)

Dresden=df[df['City'].str.startswith('Dresden')]
Dresden=Dresden.reset_index(drop=True)

Erfurt=df[df['City'].str.startswith('Erfurt')]
Erfurt=Erfurt.reset_index(drop=True)

Hamburg=df[df['City'].str.startswith('Hamburg')]
Hamburg=Hamburg.reset_index(drop=True)

Hannover=df[df['City'].str.startswith('Hannover')]
Hannover=Hannover.reset_index(drop=True)

Magdeburg=df[df['City'].str.startswith('Magdeburg')]
Magdeburg=Magdeburg.reset_index(drop=True)

Munich=df[df['City'].str.startswith('Munich')]
Munich=Munich.reset_index(drop=True)

Nuremberg=df[df['City'].str.startswith('Nuremberg')]
Nuremberg=Nuremberg.reset_index(drop=True)

Saarbruecken = df[df['City'].str.startswith('Saarbrücken')]
Saarbruecken=Saarbruecken.reset_index(drop=True)

Stuttgart=df[df['City'].str.startswith('Stuttgart')]
Stuttgart=Stuttgart.reset_index(drop=True)

print(Chemnitz)
#Saarbruecken.to_csv(r'C:\Users\lenem\Documents\Dokumente\TH\3_Semester\Data_Modelling\wasser_cleaning\Saarbruecken.csv',)

Chemnitz['Daily mean'] = pd.to_numeric(Chemnitz['Daily mean'], errors='coerce')
Chemnitz.set_index('Year')['Daily mean'].plot(kind='bar', title='Kokain Konsum Chemnitz', color='skyblue')
plt.ylabel('Daily mean')
plt.show()



# Jetzt plotten
#Chemnitz['Daily mean'].plot(kind='hist', bins=20, title='Kokain Konsum', color='skyblue')
#plt.show()
