
include ../.env

imageG:
	docker build -t jupyter-gpu \
	    --file Dockerfile-gpu \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
		singleuser

imageR:
	docker build -t jupyter-r \
	    --file Dockerfile-r \
		singleuser
imageD:
	docker build -t jupyter-devel \
	    --file Dockerfile-devel \
		singleuser

imageRS:
	docker build -t jupyter-rstudio \
	    --file Dockerfile-rstudio \
		singleuser

imageS:
	docker build -t jupyter-snpimpute \
	    --file Dockerfile-snpimpute \
		singleuser

imageM:
	docker build -t jupyter-minimal \
	    --file Dockerfile-minimal \
		singleuser

imageZ:
	docker build -t jupyter-deepzoom \
	    --file Dockerfile-deepzoom \
		singleuser

imageF:
	docker build -t jupyter-full \
	    --file Dockerfile-full \
		singleuser

imageP:
	docker build -t jupyter-pgweb \
	    --file Dockerfile-pgweb \
		singleuser

build: check-files network volumes
	docker-compose build
