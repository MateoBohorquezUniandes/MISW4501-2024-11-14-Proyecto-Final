FROM python:3.9

ADD ./src/indicadores ./src/indicadores
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/indicadores/Pipfile pipenv install --system --deploy

EXPOSE 3011/tcp
CMD [ "flask", "--app", "./src/indicadores/app", "run", "--host=0.0.0.0", "-p", "3060"]

LABEL author="i.bohorquezp@uniandes.edu.co"
