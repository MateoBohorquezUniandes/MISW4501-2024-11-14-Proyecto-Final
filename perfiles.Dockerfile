FROM python:3.9

ADD ./src/perfiles ./src/perfiles
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/perfiles/Pipfile pipenv install --system --deploy

EXPOSE 3021/tcp
CMD [ "flask", "--app", "./src/perfiles/app", "run", "--host=0.0.0.0", "-p", "3021"]

LABEL author="s.cortes@uniandes.edu.co"