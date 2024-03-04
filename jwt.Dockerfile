FROM python:3.9

ADD ./src/jwt_api_auth ./src/jwt_api_auth
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN PIPENV_PIPFILE=./src/jwt_api_auth/Pipfile pipenv install --system --deploy

EXPOSE 3000/tcp

CMD [ "flask", "--app", "./src/jwt_api_auth/app", "run", "--host=0.0.0.0", "-p", "3000"]

LABEL author="i.bohorquezp@uniandes.edu.co"