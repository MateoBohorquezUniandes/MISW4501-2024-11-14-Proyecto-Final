FROM python:3.9

ADD ./src/eventos ./src/eventos
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/eventos/Pipfile pipenv install --system --deploy

EXPOSE 3080/tcp
CMD [ "flask", "--app", "./src/eventos/app", "run", "--host=0.0.0.0", "-p", "3080"]

LABEL author="m.castros@uniandes.edu.co"