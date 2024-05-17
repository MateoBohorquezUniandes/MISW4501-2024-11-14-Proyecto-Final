FROM python:3.9

ADD ./src/notificaciones ./src/notificaciones
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/notificaciones/Pipfile pipenv install --system --deploy

EXPOSE 3050/tcp
CMD [ "flask", "--app", "./src/notificaciones/app", "run", "--host=0.0.0.0", "-p", "3050"]

LABEL author="m.castros@uniandes.edu.co"
