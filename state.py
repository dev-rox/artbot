import os
import json
import random
import pickle

def save(id):
    arquivo = open("ids.json", "r")
    json_object = json.load(arquivo)
    arquivo.close()
    json_object.append(id)
    arquivo = open("ids.json", "w")
    json.dump(json_object, arquivo)
    arquivo.close()

    

def check(id):
    arquivo = open("ids.json", "r")
    json_object = json.load(arquivo)
    if(json_object.count(id) == 0):
        return False
    else:
        return True

    




