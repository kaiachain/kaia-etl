FROM python:3.7
MAINTAINER Chan Hong <chan.hong@krustuniverse.com>
ENV PROJECT_DIR=klaytn-etl

RUN mkdir /$PROJECT_DIR
WORKDIR /$PROJECT_DIR
COPY . .
RUN pip install --upgrade pip && pip install -e /$PROJECT_DIR/

ENTRYPOINT ["python", "klaytnetl"]
