FROM python:3.9

ADD ./src/productos ./src/productos
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/productos/Pipfile pipenv install --system --deploy

EXPOSE 3090/tcp
CMD [ "flask", "--app", "./src/productos/app", "run", "--host=0.0.0.0", "-p", "3090"]

LABEL author="i.bohorquezp@uniandes.edu.co"