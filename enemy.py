'''
Enemy Timings
Takes songname and fetches the enemy timing list from ./json
'''

import json

JSONPATH = "./json/"

def returnEnemyList(SONGNAME):
    with open(JSONPATH + SONGNAME + '.json') as file:
         enemiesToCome = json.load(file)
    return enemiesToCome
