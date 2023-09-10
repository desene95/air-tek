#!/bin/sh

file_name=docker_images.txt

touch $file_name

docker ps >> $file_name

web_image_name=`awk '{ print $2 }' $file_name | tail -2 | head -1`
api_image_name=`awk '{ print $2 }' $file_name | tail -1`

echo $web_image_name
echo $api_image_name
#push web api image
aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 787257093414.dkr.ecr.ca-central-1.amazonaws.com

docker tag $api_image_name:latest 787257093414.dkr.ecr.ca-central-1.amazonaws.com/air_tek_registry-2c27200:$api_image_name
docker push 787257093414.dkr.ecr.ca-central-1.amazonaws.com/air_tek_registry-2c27200:$api_image_name


docker tag $web_image_name:latest 787257093414.dkr.ecr.ca-central-1.amazonaws.com/air_tek_registry-2c27200:$web_image_name
docker push 787257093414.dkr.ecr.ca-central-1.amazonaws.com/air_tek_registry-2c27200:$web_image_name


