Run Container:

1. Create Image

$ docker build -t flotte:latest .

2. Run Image

docker run --name flotte -d -p 8000:5000 --rm flotte:latest

3. Access service

visit -> 127.0.0.1:8000
login ->
email: admin@jku-linien.at
pwd: admin