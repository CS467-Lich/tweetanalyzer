"""
Helper function to build array with classification of element.
Cord Meados
2019
"""

import json
import numpy as np

def classification(classification):

    with open('Data/Activism_Final_Positive.json') as f:
        act_data = json.load(f)
        d1_act = len(act_data['text'])

    with open('Data/Ads_Final_Positive.json') as f:
        ads_data = json.load(f)
        d2_ads = len(ads_data['text'])

    with open('Data/Fitness_Final_Positive.json') as f:
        fit_data = json.load(f)
        d3_fit = len(fit_data['text'])

    with open('Data/Humour_Final_Positive.json') as f:
        hum_data = json.load(f)
        d4_hum = len(hum_data['text'])

    with open('Data/Political_Final_Positive_Slim.json') as f:
        pol_data = json.load(f)
        d5_pol = len(pol_data['text'])

    with open('Data/Tech_Final_Positive.json') as f:
        tec_data = json.load(f)
        d6_tec = len(tec_data['text'])


    sum = d1_act + d2_ads + d3_fit + d4_hum + d5_pol + d6_tec
    clazz = np.zeros(sum)

    if str(classification) == 'Activism':
        for i in range(0, d1_act):
            clazz[i] = 1
    if str(classification) == 'Ads':
        for i in range(d1_act, d2_ads):
            clazz[i] = 1
    if str(classification) == 'Fitness':
        for i in range(d2_ads, d3_fit):
            clazz[i] = 1
    if str(classification) == 'Humour':
        for i in range(d3_fit, d4_hum):
            clazz[i] = 1
    if str(classification) == 'Political':
        for i in range(d4_hum, d5_pol):
            clazz[i] = 1
    if str(classification) == 'Tech':
        for i in range(d5_pol, sum):
            clazz[i] = 1

    return clazz
