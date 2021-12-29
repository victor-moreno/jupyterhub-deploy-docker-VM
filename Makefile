# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

imageM:
	docker build -t jupyter-minimal \
	    --file singleuser/Dockerfile-minimal \
		singleuser
imageD:
	docker build -t jupyter-dl \
	    --file singleuser/Dockerfile-dl \
		singleuser
imageF:
	docker build -t jupyter-full \
	    --file singleuser/Dockerfile-full \
		singleuser
imageG:
	docker build -t jupyter-gpu \
	    --file singleuser/Dockerfile-gpu \
		singleuser
imageR363:
	docker build -t jupyter-r363 \
	    --file singleuser/Dockerfile-r363 \
		singleuser
imageRS363:
	docker build -t jupyter-rs363 \
	    --file singleuser/Dockerfile-rs363 \
		singleuser
imageR405:
	docker build -t jupyter-r405 \
	    --file singleuser/Dockerfile-r405 \
		singleuser
imageRS405:
	docker build -t jupyter-rs405 \
	    --file singleuser/Dockerfile-rs405 \
		singleuser
imageR412:
	docker build -t jupyter-r412 \
	    --file singleuser/Dockerfile-r412 \
		singleuser
imageRS412:
	docker build -t jupyter-rs412 \
	    --file singleuser/Dockerfile-rs412 \
		singleuser

imageAll: imageM imageD imageF imageR363 imageR405 imageR412 imageRS363 imageRS405 imageRS412

imageZ:
	docker build -t jupyter-deepzoom \
	    --file singleuser/Dockerfile-deepzoom \
		singleuser

imageV:
	docker build -t jupyter-vnc \
	    --file singleuser/Dockerfile-vnc \
		singleuser

imageRefine:
	docker build -t jupyter-refine \
	    --file singleuser/Dockerfile-refine \
		singleuser

imageT:
	docker build -t jupyter-devel \
	    --file singleuser/Dockerfile-devel \
		singleuser

proxy:
	docker build -t jupyterproxy \
	    --file proxy/Dockerfile \
		proxy

build: check-files network volumes
	docker-compose build
