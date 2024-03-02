echo "#################################################################################################"
echo "                                       SportApp - $1 Image                                       "
echo "#################################################################################################"
echo "\n\n"

microservice="$1"
version="$2"
registry="$3"

if [ -z "$microservice" ]
  then
    echo "[ERROR] No se ha indicado el nombre del microservicio\n"
    echo "\t'sh create_microservice.sh <microservicio>' <version> <registry>\n\n"

    exit 1
elif [ -z "$version" ]
  then
    echo "[ERROR] No se ha indicado la version del microservicio\n"
    echo "\t'sh create_microservice.sh <microservicio>' <version> <registry>\n\n"

    exit 1
elif [ -z "$registry" ]
  then
    echo "[ERROR] No se ha indicado el registry de publicacion\n"
    echo "\t'sh create_microservice.sh <microservicio>' <version> <registry>\n\n"

    exit 1
fi

image_path=$registry/${microservice}-api:${version}

echo "\n[$microservice] Building image for $microservice-api:$version"
docker build --platform=linux/amd64 -t $image_path ./${components[i]}

echo "\n[$microservice] Pushing image to container registry"
docker push $image_path

echo "\n[$microservice] Setup Finished Successfully\n"
echo "                                        Completed $1 Image                                        "
echo "################################################################################################\n"
exit 0
