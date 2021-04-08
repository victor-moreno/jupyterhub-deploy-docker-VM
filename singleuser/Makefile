
include ../.env

imageG:
	docker build -t jupyter-gpu \
	    --file Dockerfile-gpu \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
		.

imageR:
	docker build -t jupyter-r \
	    --file Dockerfile-r \
		.
imageD:
	docker build -t jupyter-devel \
	    --file Dockerfile-devel \
		.

imageRS:
	docker build -t jupyter-rstudio \
	    --file Dockerfile-rstudio \
		.

imageS:
	docker build -t jupyter-snpimpute \
	    --file Dockerfile-snpimpute \
		.

imageM:
	docker build -t jupyter-minimal \
	    --file Dockerfile-minimal \
		.

imageZ:
	docker build -t jupyter-deepzoom \
	    --file Dockerfile-deepzoom \
		.

imageF:
	docker build -t jupyter-full \
	    --file Dockerfile-full \
		.

imageP:
	docker build -t jupyter-pgweb \
	    --file Dockerfile-pgweb \
		.
imageV:
	docker build -t jupyter-vnc \
	    --file Dockerfile-vnc \
		.


all14:	imageF imageM imageP imageR imageRS imageS imageZ imageV imageG imageD 
all00:	imageF imageM imageP imageR imageRS imageS imageZ imageV
