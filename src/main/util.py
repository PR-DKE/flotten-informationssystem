import requests

from main.models import Zug, Personenwaggon, Triebwagen

def get_trains():
    r = requests.get('http://localhost:5000/api/train')
    print(r.text)
    for train in r.json().get('trains'):
        print(train.get('id'))
        print(train.get('waggons'))
        print(train.get('sitze'))
        print(train.get('spurweite'))
        print(train.get('url'))
