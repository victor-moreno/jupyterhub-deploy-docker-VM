# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

imageG:
	docker build -t jupyter-gpu \
	    --file singleuser/Dockerfile-gpu \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
		singleuser

imageC:
	docker build -t jupyter-cuda \
	    --file singleuser/Dockerfile-cuda \
		singleuser
imageT:
	docker build -t jupyter-torch \
	    --file singleuser/Dockerfile-torch \
		singleuser
imageR:
	docker build -t jupyter-r \
	    --file singleuser/Dockerfile-r \
		singleuser
imageD:
	docker build -t jupyter-devel \
	    --file singleuser/Dockerfile-devel \
		singleuser

imageRS:
	docker build -t jupyter-rstudio \
	    --file singleuser/Dockerfile-rs \
		singleuser

imageRStudio:
	docker build -t jupyter-rstudio \
	    --file singleuser/Dockerfile-rstudio \
		singleuser

imageRSlatest:
	docker build -t jupyter-rstudio \
	    --file singleuser/Dockerfile-rslatest \
		singleuser

imageS:
	docker build -t jupyter-snpimpute \
	    --file singleuser/Dockerfile-snpimpute \
		singleuser

imageM:
	docker build -t jupyter-minimal \
	    --file singleuser/Dockerfile-minimal \
		singleuser

imageZ:
	docker build -t jupyter-deepzoom \
	    --file singleuser/Dockerfile-deepzoom \
		singleuser

imageF:
	docker build -t jupyter-full \
	    --file singleuser/Dockerfile-full \
		singleuser

imageP:
	docker build -t jupyter-pgweb \
	    --file singleuser/Dockerfile-pgweb \
		singleuser

imageV:
	docker build -t jupyter-vnc \
	    --file singleuser/Dockerfile-vnc \
		singleuser

proxy:
	docker build -t jupyterproxy \
	    --file proxy/Dockerfile \
		proxy

build: check-files network volumes
	docker-compose build
