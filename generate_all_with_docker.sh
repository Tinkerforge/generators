#!/bin/bash

ROOT_DIR=`/bin/pwd`
DAEMONLIB_DIR=$(realpath $ROOT_DIR/../daemonlib)

if command -v docker >/dev/null 2>&1 ; then
	if [ $(/usr/bin/docker images -q tinkerforge/build_environment_full) ]; then
		echo "Using docker image to build.";
		docker run \
		-v $ROOT_DIR/../:/$ROOT_DIR/../ -u $(id -u):$(id -g) \
		tinkerforge/build_environment_full /bin/bash \
		-c "cd $ROOT_DIR ; python3 generate_all.py "$@""; \
	else
		echo "No docker image found.";
	fi
else
	echo "Docker not found";
fi
