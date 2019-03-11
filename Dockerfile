FROM pablomacias/s2t_main-controller

WORKDIR /srv/S2T/S2T_MainController

ADD . .

RUN apk add --update swig git bsd-compat-headers
RUN pip install numpy
RUN pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master
RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


