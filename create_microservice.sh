echo "#################################################################################################"
echo "                                       SportApp - $1 Setup                                       "
echo "#################################################################################################"
echo "\n\n"

if [ -z "$1" ]
  then
    echo "[ERROR] No se ha indicado el nombre del microservicio\n"
    echo "\t'sh create_microservice.sh <microservicio>'\n\n"

    exit 1
fi


mkdir src/$1
touch src/$1/__init__.py
touch src/$1/app.py

mkdir src/$1/application
touch src/$1/application/__init__.py
touch src/$1/application/mappers.py
mkdir src/$1/application/commands
touch src/$1/application/commands/__init__.py
mkdir src/$1/application/queries
touch src/$1/application/queries/__init__.py

mkdir src/$1/domain
touch src/$1/domain/__init__.py
touch src/$1/domain/entities.py
touch src/$1/domain/events.py
touch src/$1/domain/exceptions.py
touch src/$1/domain/factories.py
touch src/$1/domain/repositories.py
touch src/$1/domain/rules.py
touch src/$1/domain/value_objects.py

mkdir src/$1/infrastructure
touch src/$1/infrastructure/__init__.py
mkdir src/$1/infrastructure/schema
touch src/$1/infrastructure/schema/__init__.py
touch src/$1/infrastructure/consumers.py
touch src/$1/infrastructure/dispatchers.py
touch src/$1/infrastructure/dtos.py
touch src/$1/infrastructure/exceptions.py
touch src/$1/infrastructure/factories.py
touch src/$1/infrastructure/mappers.py
touch src/$1/infrastructure/repositories.py


mkdir src/$1/presentation
touch src/$1/presentation/__init__.py
touch src/$1/presentation/api.py
touch src/$1/presentation/handlers.py

touch ./$1.Dockerfile

echo "                                        Completed $1 Setup                                        "
echo "################################################################################################\n"
exit 0
