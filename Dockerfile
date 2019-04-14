FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG G2P_NAME
ENV G2P_NAME = $G2P_NAME

WORKDIR /srv/S2T/S2T_G2P

ADD . .

RUN apk add --update swig git bsd-compat-headers
RUN pip install numpy
RUN pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master
RUN pip install -r requirements.txt

CMD python src/app.py $G2P_NAME $SHARED_FOLDER


