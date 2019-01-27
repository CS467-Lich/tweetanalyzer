'''
Helper functions
CS467 Lich
Cord Meados 2019
'''

import json

# CONSTANTS
# file we want to write to. This could be updated to reference an outside file.
myDataFile = 'data.json'


#HELPER FUNCTIONS
# write data as JSON to file
def writeAsJSON(data):
    with open(myDataFile, 'w') as outfile:
        json.dump(data, outfile)










# References
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
