# flotten-informationssystem

Flask-Applikation zur Verwaltung von Zügen, Waggons, Wartungen und Mitarbeitern.

## Download
```
$ git clone https://github.com/PR-DKE/flotten-informationssystem/
```

## Installation der Applikation als Docker Container[^1]:

1. **Create Image** [^2]

```
$ cd <path-to-root-folder>
$ docker build -t flotte:latest .
```

2. **Run Image**
```
$ docker run --name flotte -d -p 8000:5000 --rm flotte:latest
```

3. **Access service**

> 127.0.0.1:8000

email: **admin@jku-linien.at**

pwd: **admin**

[^1]: Die Applikation läuft als Container eventuell etwas langsam. Die lokale Ausführung garantiert ein besseres Erlebnis.
[^2]: Auf Windows Systemen kann es zu Problemen mit der Script-Datei kommen **ANLEITUNG ERGÄNZEN!**.

## Ausführen der Applikation lokal:

Alle benötigten dependencies befinden sich in der virtuellen [Python Umgebung].
Alternativ kann natürlich eine eigene VENV initialisiert werden, eine Auflistung der benoetigten Packages befindet sich in den [Requirements].

1. **Venv starten**
```
$ cd <path-to-root-folder>
$ source venv/bin/activate
```

2. **FLASK_APP EV setzen**
```
$ EXPORT FLASK_APP = src/flotten.py
```
3. **Applikation starten**
```
$ flask run
```

email: **admin@jku-linien.at**

pwd: **admin**

[Python Umgebung]: /venv
[Requirements]: /requirements.txt
