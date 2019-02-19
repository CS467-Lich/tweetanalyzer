import pandas as pd
from stitch_funcs import stitch

"""
DATA_FOLDER = 'Unit_Test_Files/'
FILES = {
	'Activism': 'activism_test.json',
	'Advertisement': 'ads_test.json',
	'Fitness': 'fitness_test.json',
	'Humor': 'humor_test.json',
	'Political': 'political_test.json',
	'Technology': 'tech_test.json'	
}
"""

DATA_FOLDER = 'Final_Positives/'
FILES = {
	'Activism': 'Activism_Final_Positive.json',
	'Advertisement': 'Ads_Final_Positive.json',
	'Fitness': None,
	'Humor': 'Humour_Final_Positive.json',
	'Political': 'Political_Final_Positive.json',
	'Technology': 'Tech_Final_Positive.json'
}

combinedData = stitch(DATA_FOLDER, FILES)

df = pd.DataFrame.from_dict(combinedData)
print(df)