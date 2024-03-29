FROM python:3.9

ADD ./src/planes ./src/planes
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/planes/Pipfile pipenv install --system --deploy

EXPOSE 3015/tcp
CMD [ "flask", "--app", "./src/planes/app", "run", "--host=0.0.0.0", "-p", "3015"]

LABEL author="h.patarroyo@uniandes.edu.co"