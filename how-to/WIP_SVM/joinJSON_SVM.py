'''
Joining JSON files in folder.
CS467 Lich
Cord Meados 2019
'''

import json
import os
from helperFunctions import writeAsJSON
from jsonmerge import Merger


MY_DATA_FOLDER = "Data"
MY_FINAL_DATA = 'Final_Positive.json'

# storing all the json data here

finalJSON = {}

# Prepare merger. https://pypi.org/project/jsonmerge/
schema = {
        "properties": {
            "user": {"mergeStrategy": "append"},
            "date": {"mergeStrategy": "append"},
            "text": {"mergeStrategy": "append"},
            "source": {"mergeStrategy": "append"},
            "coordinates": {"mergeStrategy": "append"},
            "language": {"mergeStrategy": "append"},
            "hashtags": {"mergeStrategy": "append"},
        }
}
merger = Merger(schema)

# import json data files and join them into "finalJSON"
for filename in os.listdir(MY_DATA_FOLDER):
    # print(filename)
    with open(MY_DATA_FOLDER + '/' + filename) as f:
        tempJSONData = json.load(f)
    finalJSON = merger.merge(finalJSON, tempJSONData)

# store final json data
writeAsJSON(finalJSON, MY_DATA_FOLDER + '/' + MY_FINAL_DATA)

# References
# https://pypi.org/project/jsonmerge/
