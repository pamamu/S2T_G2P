FROM python:3.6-alpine

WORKDIR /srv/S2T/S2T_MainController

ADD . .

RUN apk add --update build-base swig git bsd-compat-headers
RUN pip install numpy
RUN pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master
RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]

