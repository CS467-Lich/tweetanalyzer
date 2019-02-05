'''
Helper functions
CS467 Lich
Cord Meados 2019
'''

#####################################################
# imports
import json


#####################################################
# CONSTANTS


#####################################################
#HELPER FUNCTIONS
"""
write data as JSON to file.
Parameters:
data: data you want written to the file
filename: the filepath the data will be written to
"""
def writeAsJSON(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)





# References
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
