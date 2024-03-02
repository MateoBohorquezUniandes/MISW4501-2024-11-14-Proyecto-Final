FROM python:3.9

ADD ./src/monitor ./src/monitor


RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/monitor/Pipfile pipenv install --system --deploy

EXPOSE 3200/tcp
CMD [ "flask", "--app", "./src/monitor/app", "run", "--host=0.0.0.0", "-p", "3200"]

LABEL author="m.castros@uniandes.edu.co"