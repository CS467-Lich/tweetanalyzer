"""
Slims down data
Cord Meados
2019
"""

import json
import math

with open('Data/Political_Final_Positive.json') as f:
    pol_data = json.load(f)


for i in range(0, math.floor(len(pol_data['text'])/4)):
    if i % 4 != 0:
        del pol_data['text'][i]

with open("Data/Political_Final_Positive_Slim.json", "w") as file:
    json.dump(pol_data, file,  indent=4)
    file.close()


