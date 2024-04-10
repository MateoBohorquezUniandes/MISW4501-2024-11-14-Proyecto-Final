FROM python:3.9

ADD ./src/planes ./src/planes
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/planes/Pipfile pipenv install --system --deploy

EXPOSE 3021/tcp
CMD [ "flask", "--app", "./src/planes/app", "run", "--host=0.0.0.0", "-p", "3030"]

LABEL author="s.cortes@uniandes.edu.co"