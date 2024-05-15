FROM python:3.9

# inject credentials as environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=./src/service-account.json

# install the Google Cloud SDK
RUN curl -sSL https://sdk.cloud.google.com | bash

ADD ./src/notificaciones ./src/notificaciones
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/notificaciones/Pipfile pipenv install --system --deploy

EXPOSE 3050/tcp
CMD [ "flask", "--app", "./src/notificaciones/app", "run", "--host=0.0.0.0", "-p", "3050"]

LABEL author="m.castros@uniandes.edu.co"
