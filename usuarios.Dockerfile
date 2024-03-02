FROM python:3.9

ADD ./src/usuarios ./src/usuarios
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/usuarios/Pipfile pipenv install --system --deploy

EXPOSE 3011/tcp
CMD [ "flask", "--app", "./src/usuarios/app", "run", "--host=0.0.0.0", "-p", "3011"]

LABEL author="h.patarroyo@uniandes.edu.co"