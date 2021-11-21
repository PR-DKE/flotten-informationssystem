import requests

from main.models import Zug, Personenwaggon, Triebwagen


def calculate_sitze(zug):
    summe=0
    waggons=Personenwaggon.query.filter_by(zug_id=zug)
    for waggon in waggons:
        summe = summe + waggon.sitzanzahl
    return summe

def calculate_waggons(zug):
    summe=0
    waggons=Personenwaggon.query.filter_by(zug_id=zug)
    for waggon in waggons:
        summe+=1
    return summe

def calculate_maxgewicht(zug):
    summe=0
    waggons=Personenwaggon.query.filter_by(zug_id=zug)
    for waggon in waggons:
        summe = summe + waggon.maxGewicht
    return summe

def get_spurweite(zug):
    z = Zug.query.get(zug)
    w = Triebwagen.query.get(z.triebwagen)
    return w.spurweite

def get_trains():
    r = requests.get('http://localhost:5000/api/train')
    print(r.text)
    for train in r.json().get('trains'):
        print(train.get('id'))
        print(train.get('waggons'))
        print(train.get('sitze'))
        print(train.get('spurweite'))
        print(train.get('url'))
