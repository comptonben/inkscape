FROM python:3.9

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system

RUN useradd -ms /bin/bash inkscape
USER inkscape