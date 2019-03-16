import pandas as pd
import json


files = ["activism", "ads", "comedy", "fitness", "politics", "tech"]

#Convert JSON files

with open('activism.json') as f:
   data = json.load(f)

df1 = pd.DataFrame(data)
df1.to_csv("activism.csv")

with open('ads.json') as f:
   data = json.load(f)

df2 = pd.DataFrame(data)
df2.to_csv("ads.csv")

with open('comedy.json') as f:
   data = json.load(f)

df3 = pd.DataFrame(data)
df3.to_csv("comedy.csv")

with open('fitness.json') as f:
   data = json.load(f)

df4 = pd.DataFrame(data)
df4.to_csv("fitness.csv")

with open('politics.json') as f:
   data = json.load(f)

df5 = pd.DataFrame(data)
df5.to_csv("politics.csv")

with open('tech.json') as f:
   data = json.load(f)

df6 = pd.DataFrame(data)
df6.to_csv("tech.csv")


#Add correct category to each file
for file in files:
	csv_input = pd.read_csv(file + '.csv')
	csv_input['Category'] = file
	csv_input.to_csv(file + 'output.csv', index=False)



#Combine all files
ndf1 = pd.read_csv('activismoutput.csv', index_col=None)
ndf2 = pd.read_csv('adsoutput.csv', index_col=None)
ndf3 = pd.read_csv('comedyoutput.csv', index_col=None)
ndf4 = pd.read_csv('fitnessoutput.csv', index_col=None)
ndf5 = pd.read_csv('politicsoutput.csv', index_col=None)
ndf6 = pd.read_csv('techoutput.csv', index_col=None)




finaldf = pd.concat([df1, df2, df3, df4, df5, df6], axis=0)
finaldf.to_csv('All_Positive.csv', index=False)
