from main.models import Zug, Personenwaggon


def calculate_sitze(zug):
    summe=0
    waggons=Personenwaggon.query.filter_by(zug_id=zug)
    for waggon in waggons:
        summe = summe + waggon.sitzanzahl
    return summe