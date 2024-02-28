FROM python:3.11

ADD ./src/perfiles ./src/perfiles
ADD ./src/seedwork ./src/seedwork

RUN pip install pipenv
RUN pipenv install --system --deploy

EXPOSE 3001/tcp
CMD [ "flask", "--app", "./src/perfiles/app", "run", "--host=0.0.0.0", "-p", "3001"]

LABEL author="s.cortes@uniandes.edu.co"