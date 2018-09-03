#!/bin/bash

ROOT_DIR=`/bin/pwd`

if [ -t 0 ]; then
	DOCKER_FLAGS="-it"
else
	DOCKER_FLAGS=
fi

if command -v docker >/dev/null 2>&1 ; then
	if [ $(/usr/bin/docker images -q tinkerforge/build_environment_full) ]; then
		echo "Using docker image to build."
		docker run $DOCKER_FLAGS \
		-v $ROOT_DIR/../:/$ROOT_DIR/../ -u $(id -u):$(id -g) \
		tinkerforge/build_environment_full /bin/bash \
		-c "cd $ROOT_DIR ; python3 -u generate_all.py "$@""
	else
		echo "No docker image found."
	fi
else
	echo "Docker not found."
fi
