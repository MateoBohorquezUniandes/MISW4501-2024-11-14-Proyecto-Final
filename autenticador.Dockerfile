FROM python:3.9

ADD ./src/autenticador ./src/autenticador
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/autenticador/Pipfile pipenv install --system --deploy

EXPOSE 3000/tcp

CMD [ "flask", "--app", "./src/autenticador/app", "run", "--host=0.0.0.0", "-p", "3000"]

LABEL author="i.bohorquezp@uniandes.edu.co"
