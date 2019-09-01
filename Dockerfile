FROM python:3.6

RUN apt-get update
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $buildDeps

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

