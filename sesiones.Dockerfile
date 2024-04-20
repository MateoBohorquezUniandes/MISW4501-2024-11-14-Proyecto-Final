FROM python:3.9

ADD ./src/sesiones ./src/sesiones
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/sesiones/Pipfile pipenv install --system --deploy

EXPOSE 3011/tcp
CMD [ "flask", "--app", "./src/sesiones/app", "run", "--host=0.0.0.0", "-p", "3070"]

LABEL author="s.cortes@uniandes.edu.co"
