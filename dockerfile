FROM python:slim

WORKDIR /home/flotten-informationssystem

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY src/main src/main
COPY migrations migrations
COPY src/flotten.py src/config.py src/
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP src/flotten.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]